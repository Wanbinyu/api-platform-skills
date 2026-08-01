#!/usr/bin/env python3
"""
openapi_breaking_diff.py - structural OpenAPI 3.x change classifier.

Helps breaking-change-review by listing discrete deltas with a provisional class.
Human/agent still owns migration notes and final merge verdict.

Usage:
  python scripts/openapi_breaking_diff.py old.yaml new.yaml
  python scripts/openapi_breaking_diff.py old.yaml new.yaml --format json
  python scripts/openapi_breaking_diff.py old.yaml new.yaml --markdown report.md

Exit codes:
  0 - no hard/semantic breaks (additive-only or empty)
  2 - at least one breaking or semantic-breaking delta
  1 - usage / parse error
"""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)


# ---------------------------------------------------------------------------
# Load / resolve
# ---------------------------------------------------------------------------

def load_spec(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return data


def resolve_ref(root: dict[str, Any], node: Any, stack: tuple[str, ...] = ()) -> Any:
    if not isinstance(node, dict):
        return node
    if "$ref" in node and isinstance(node["$ref"], str):
        ref = node["$ref"]
        if not ref.startswith("#/"):
            return node  # external refs: leave as-is
        if ref in stack:
            return {"$ref": ref, "_cycle": True}
        cur: Any = root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(cur, dict) or part not in cur:
                return node
            cur = cur[part]
        merged = resolve_ref(root, deepcopy(cur), stack + (ref,))
        # sibling keys beside $ref (OpenAPI 3.1 style) — shallow merge
        extras = {k: v for k, v in node.items() if k != "$ref"}
        if extras and isinstance(merged, dict):
            out = deepcopy(merged)
            out.update(extras)
            return out
        return merged
    out: dict[str, Any] = {}
    for k, v in node.items():
        out[k] = resolve_ref(root, v, stack)
    return out


def schema_props(schema: Any) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    if schema.get("type") == "object" or "properties" in schema:
        return dict(schema.get("properties") or {})
    # allOf: shallow merge properties
    props: dict[str, Any] = {}
    for part in schema.get("allOf") or []:
        props.update(schema_props(part))
    props.update(dict(schema.get("properties") or {}))
    return props


def schema_required(schema: Any) -> set[str]:
    if not isinstance(schema, dict):
        return set()
    req = set(schema.get("required") or [])
    for part in schema.get("allOf") or []:
        req |= schema_required(part)
    return req


def schema_type(schema: Any) -> str:
    if not isinstance(schema, dict):
        return type(schema).__name__
    if "$ref" in schema:
        return f"ref:{schema['$ref']}"
    t = schema.get("type")
    if isinstance(t, list):
        t = "|".join(str(x) for x in t)
    fmt = schema.get("format")
    enum = schema.get("enum")
    bits = [str(t or "any")]
    if fmt:
        bits.append(f"fmt:{fmt}")
    if enum is not None:
        bits.append("enum")
    return "/".join(bits)


def json_pointer_escape(s: str) -> str:
    return s.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------------------
# Extract operations
# ---------------------------------------------------------------------------

HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


def iter_operations(spec: dict[str, Any]):
    paths = spec.get("paths") or {}
    if not isinstance(paths, dict):
        return
    for path, item in paths.items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(op, dict):
                continue
            yield path, method.lower(), op


def op_security(spec: dict[str, Any], op: dict[str, Any]) -> list[Any]:
    if "security" in op:
        return op.get("security") or []
    return spec.get("security") or []


def request_schema(root: dict[str, Any], op: dict[str, Any]) -> Any:
    rb = op.get("requestBody")
    if not rb:
        return None
    rb = resolve_ref(root, rb)
    content = (rb or {}).get("content") or {}
    for ct in ("application/json", "application/*+json"):
        if ct in content:
            return resolve_ref(root, content[ct].get("schema"))
    # first content schema
    for _, media in content.items():
        if isinstance(media, dict) and "schema" in media:
            return resolve_ref(root, media.get("schema"))
    return None


def response_schemas(root: dict[str, Any], op: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    responses = op.get("responses") or {}
    for code, resp in responses.items():
        resp = resolve_ref(root, resp)
        if not isinstance(resp, dict):
            continue
        content = resp.get("content") or {}
        schema = None
        for ct, media in content.items():
            if isinstance(media, dict) and "schema" in media:
                schema = resolve_ref(root, media.get("schema"))
                break
        out[str(code)] = schema
    return out


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------

class Delta(dict):
    """delta dict with stable keys for JSON/MD."""


def add_delta(
    deltas: list[Delta],
    *,
    kind: str,
    cls: str,
    path: str,
    detail: str,
    impact: str = "",
) -> None:
    deltas.append(
        Delta(
            id=len(deltas) + 1,
            kind=kind,
            class_=cls,  # renamed on emit
            path=path,
            detail=detail,
            impact=impact
            or (
                "clients may break"
                if cls in ("breaking", "semantic-breaking")
                else "usually safe"
            ),
        )
    )


def compare_schemas(
    deltas: list[Delta],
    old_s: Any,
    new_s: Any,
    loc: str,
    *,
    side: str,
) -> None:
    """side: request | response"""
    if old_s is None and new_s is None:
        return
    if old_s is not None and new_s is None:
        add_delta(
            deltas,
            kind="schema_removed",
            cls="breaking",
            path=loc,
            detail=f"{side} schema removed",
        )
        return
    if old_s is None and new_s is not None:
        add_delta(
            deltas,
            kind="schema_added",
            cls="non-breaking",
            path=loc,
            detail=f"{side} schema added",
            impact="clients may ignore",
        )
        return

    old_t, new_t = schema_type(old_s), schema_type(new_s)
    if old_t != new_t and "ref:" not in old_t and "ref:" not in new_t:
        # money/unit smell
        cls = "semantic-breaking" if {"integer", "number"} & {old_t.split("/")[0], new_t.split("/")[0]} else "breaking"
        add_delta(
            deltas,
            kind="type_change",
            cls=cls,
            path=loc,
            detail=f"{side} type {old_t} -> {new_t}",
        )

    # arrays: recurse into items
    if isinstance(old_s, dict) and isinstance(new_s, dict):
        if "items" in old_s or "items" in new_s:
            compare_schemas(
                deltas,
                old_s.get("items") if isinstance(old_s, dict) else None,
                new_s.get("items") if isinstance(new_s, dict) else None,
                f"{loc}[]",
                side=side,
            )

    old_props, new_props = schema_props(old_s), schema_props(new_s)
    old_req, new_req = schema_required(old_s), schema_required(new_s)

    for name in sorted(set(old_props) - set(new_props)):
        add_delta(
            deltas,
            kind="property_removed",
            cls="breaking",
            path=f"{loc}.{name}",
            detail=f"{side} property removed: {name}",
        )
    for name in sorted(set(new_props) - set(old_props)):
        if name in new_req and side == "request":
            add_delta(
                deltas,
                kind="property_added_required",
                cls="breaking",
                path=f"{loc}.{name}",
                detail=f"request required property added: {name}",
            )
        else:
            add_delta(
                deltas,
                kind="property_added",
                cls="non-breaking",
                path=f"{loc}.{name}",
                detail=f"{side} optional property added: {name}",
            )

    for name in sorted(set(old_props) & set(new_props)):
        compare_schemas(
            deltas,
            old_props[name],
            new_props[name],
            f"{loc}.{name}",
            side=side,
        )
        # enum shrink
        oe = (old_props[name] or {}).get("enum") if isinstance(old_props[name], dict) else None
        ne = (new_props[name] or {}).get("enum") if isinstance(new_props[name], dict) else None
        if isinstance(oe, list) and isinstance(ne, list):
            removed = set(map(str, oe)) - set(map(str, ne))
            if removed:
                add_delta(
                    deltas,
                    kind="enum_removed_values",
                    cls="breaking",
                    path=f"{loc}.{name}",
                    detail=f"enum values removed: {sorted(removed)}",
                )

    # top-level enum shrink (e.g. status field schema)
    if isinstance(old_s, dict) and isinstance(new_s, dict):
        oe = old_s.get("enum")
        ne = new_s.get("enum")
        if isinstance(oe, list) and isinstance(ne, list):
            removed = set(map(str, oe)) - set(map(str, ne))
            if removed:
                add_delta(
                    deltas,
                    kind="enum_removed_values",
                    cls="breaking",
                    path=loc,
                    detail=f"enum values removed: {sorted(removed)}",
                )

    # required tighten on request
    if side == "request":
        for name in sorted(new_req - old_req):
            if name in old_props or name in new_props:
                add_delta(
                    deltas,
                    kind="required_added",
                    cls="breaking",
                    path=f"{loc}.{name}",
                    detail=f"request field became required: {name}",
                )


def security_sig(sec: list[Any]) -> str:
    if not sec:
        return "none"
    try:
        return json.dumps(sec, sort_keys=True)
    except TypeError:
        return str(sec)


def diff_specs(old: dict[str, Any], new: dict[str, Any]) -> list[Delta]:
    deltas: list[Delta] = []

    old_ops = {(p, m): op for p, m, op in iter_operations(old)}
    new_ops = {(p, m): op for p, m, op in iter_operations(new)}

    for key in sorted(set(old_ops) - set(new_ops)):
        path, method = key
        add_delta(
            deltas,
            kind="operation_removed",
            cls="breaking",
            path=f"{method.upper()} {path}",
            detail="operation removed",
        )

    for key in sorted(set(new_ops) - set(old_ops)):
        path, method = key
        add_delta(
            deltas,
            kind="operation_added",
            cls="non-breaking",
            path=f"{method.upper()} {path}",
            detail="operation added",
            impact="new surface",
        )

    for key in sorted(set(old_ops) & set(new_ops)):
        path, method = key
        loc = f"{method.upper()} {path}"
        oop, nop = old_ops[key], new_ops[key]

        # security
        os_ = security_sig(op_security(old, oop))
        ns_ = security_sig(op_security(new, nop))
        if os_ != ns_:
            # removing auth is breaking + security risk
            cls = "breaking"
            if os_ != "none" and ns_ == "none":
                detail = f"security removed (was {os_})"
            elif os_ == "none" and ns_ != "none":
                detail = f"security added ({ns_})"
                # newly required auth can break anonymous clients
            else:
                detail = f"security changed {os_} -> {ns_}"
            add_delta(
                deltas,
                kind="security_change",
                cls=cls,
                path=loc,
                detail=detail,
            )

        # success status codes (2xx)
        old_codes = {c for c in (oop.get("responses") or {}) if str(c).startswith("2")}
        new_codes = {c for c in (nop.get("responses") or {}) if str(c).startswith("2")}
        for c in sorted(old_codes - new_codes, key=str):
            add_delta(
                deltas,
                kind="success_status_removed",
                cls="breaking",
                path=loc,
                detail=f"success status {c} removed",
            )
        for c in sorted(new_codes - old_codes, key=str):
            add_delta(
                deltas,
                kind="success_status_added",
                cls="non-breaking",
                path=loc,
                detail=f"success status {c} added",
            )

        # request schema
        compare_schemas(
            deltas,
            request_schema(old, oop),
            request_schema(new, nop),
            f"{loc} request",
            side="request",
        )

        # primary success response body: prefer 200 then 201 then first 2xx
        old_resps = response_schemas(old, oop)
        new_resps = response_schemas(new, nop)
        prefer = ["200", "201", "202", "204"]
        old_code = next((c for c in prefer if c in old_resps), None)
        new_code = next((c for c in prefer if c in new_resps), None)
        if old_code and new_code and old_code != new_code:
            add_delta(
                deltas,
                kind="success_status_changed",
                cls="breaking",
                path=loc,
                detail=f"primary success status {old_code} -> {new_code}",
            )
        # compare body for codes present on both sides
        for code in sorted(set(old_resps) & set(new_resps), key=str):
            if not str(code).startswith("2"):
                continue
            compare_schemas(
                deltas,
                old_resps[code],
                new_resps[code],
                f"{loc} response[{code}]",
                side="response",
            )

    return deltas


def emit_class(d: Delta) -> str:
    return d.get("class_") or d.get("class") or "unclear"


def to_public(d: Delta) -> dict[str, Any]:
    return {
        "id": d["id"],
        "kind": d["kind"],
        "class": emit_class(d),
        "path": d["path"],
        "detail": d["detail"],
        "impact": d["impact"],
    }


def render_markdown(
    old_path: Path,
    new_path: Path,
    deltas: list[Delta],
) -> str:
    rows = []
    for d in deltas:
        rows.append(
            f"| {d['id']} | {d['path']} | {d['detail']} | **{emit_class(d)}** | {d['impact']} |"
        )
    hard = sum(1 for d in deltas if emit_class(d) in ("breaking", "semantic-breaking"))
    soft = sum(1 for d in deltas if emit_class(d) == "non-breaking")
    verdict_hint = (
        "request-changes (tool found hard/semantic breaks)"
        if hard
        else "likely approve if agent review agrees (no hard breaks detected)"
    )
    table = "\n".join(rows) if rows else "| - | - | no deltas | - | - |"
    return f"""# OpenAPI breaking diff (machine assist)

> Generated by `scripts/openapi_breaking_diff.py`.  
> **Not a final merge verdict** — feed into `breaking-change-review`.

## Scope
- Before: `{old_path.as_posix()}`
- After: `{new_path.as_posix()}`

## Summary
- Hard / semantic breaks: **{hard}**
- Non-breaking: **{soft}**
- Total deltas: **{len(deltas)}**
- Tool hint: **{verdict_hint}**

## Deltas
| # | path | detail | class | impact |
|---|------|--------|-------|--------|
{table}

## Next (agent)
1. Confirm each delta (false positives possible with complex allOf/oneOf).
2. Add migration notes or waivers for every break.
3. Emit final verdict with `breaking-change-review` template.
"""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Classify OpenAPI 3.x structural changes")
    p.add_argument("old", type=Path, help="before OpenAPI file")
    p.add_argument("new", type=Path, help="after OpenAPI file")
    p.add_argument("--format", choices=("markdown", "json", "both"), default="markdown")
    p.add_argument("--markdown", type=Path, help="write markdown report to path")
    p.add_argument("--json-out", type=Path, help="write JSON to path")
    args = p.parse_args(argv)

    try:
        old = load_spec(args.old)
        new = load_spec(args.new)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    deltas = diff_specs(old, new)
    public = [to_public(d) for d in deltas]
    md = render_markdown(args.old, args.new, deltas)

    if args.format in ("markdown", "both"):
        print(md)
    if args.format in ("json", "both"):
        print(json.dumps({"deltas": public, "hard_breaks": sum(
            1 for d in public if d["class"] in ("breaking", "semantic-breaking")
        )}, indent=2, ensure_ascii=False))

    if args.markdown:
        args.markdown.write_text(md, encoding="utf-8")
    if args.json_out:
        args.json_out.write_text(
            json.dumps({"deltas": public}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    hard = any(d["class"] in ("breaking", "semantic-breaking") for d in public)
    return 2 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())

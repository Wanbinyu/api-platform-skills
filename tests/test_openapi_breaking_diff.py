from __future__ import annotations

import unittest

from scripts.openapi_breaking_diff import diff_specs


def response(schema: object) -> dict[str, object]:
    return {
        "responses": {
            "200": {
                "description": "OK",
                "content": {"application/json": {"schema": schema}},
            }
        }
    }


def spec(path_item: dict[str, object]) -> dict[str, object]:
    return {
        "openapi": "3.0.3",
        "info": {"title": "Test", "version": "1.0.0"},
        "paths": {"/orders/{orderId}": path_item},
    }


def kinds(deltas: list[dict[str, object]]) -> set[str]:
    return {str(delta["kind"]) for delta in deltas}


class OpenApiBreakingDiffTests(unittest.TestCase):
    def test_path_level_parameter_removal_is_breaking(self) -> None:
        parameter = {
            "name": "orderId",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
        old = spec({"parameters": [parameter], "get": response({"type": "string"})})
        new = spec({"get": response({"type": "string"})})

        deltas = diff_specs(old, new)

        self.assertIn("parameter_removed", kinds(deltas))
        self.assertTrue(any(delta["class_"] == "breaking" for delta in deltas))

    def test_request_body_required_toggle_is_breaking(self) -> None:
        old_body = {
            "required": False,
            "content": {"application/json": {"schema": {"type": "object"}}},
        }
        new_body = {**old_body, "required": True}
        old = spec({"post": {**response({"type": "string"}), "requestBody": old_body}})
        new = spec({"post": {**response({"type": "string"}), "requestBody": new_body}})

        deltas = diff_specs(old, new)

        self.assertIn("request_body_required", kinds(deltas))
        self.assertTrue(any(delta["class_"] == "breaking" for delta in deltas))

    def test_request_content_type_removal_is_breaking(self) -> None:
        old_body = {
            "content": {
                "application/json": {"schema": {"type": "object"}},
                "text/plain": {"schema": {"type": "string"}},
            }
        }
        new_body = {"content": {"application/json": {"schema": {"type": "object"}}}}
        old = spec({"post": {**response({"type": "string"}), "requestBody": old_body}})
        new = spec({"post": {**response({"type": "string"}), "requestBody": new_body}})

        deltas = diff_specs(old, new)

        self.assertIn("request_content_type_removed", kinds(deltas))

    def test_nested_refs_are_compared(self) -> None:
        old = spec(
            {
                "get": response({"$ref": "#/components/schemas/Envelope"}),
            }
        )
        old["components"] = {
            "schemas": {
                "Envelope": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Order"},
                        }
                    },
                },
                "Order": {
                    "type": "object",
                    "required": ["id", "status"],
                    "properties": {"id": {"type": "string"}, "status": {"type": "string"}},
                },
            }
        }
        new = spec(
            {
                "get": response({"$ref": "#/components/schemas/Envelope"}),
            }
        )
        new["components"] = {
            "schemas": {
                "Envelope": old["components"]["schemas"]["Envelope"],  # type: ignore[index]
                "Order": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {"id": {"type": "string"}},
                },
            }
        }

        deltas = diff_specs(old, new)

        self.assertTrue(
            any(
                delta["kind"] == "property_removed" and "data[].status" in str(delta["path"])
                for delta in deltas
            )
        )

    def test_nullable_change_is_detected(self) -> None:
        old = spec({"get": response({"type": "string", "nullable": True})})
        new = spec({"get": response({"type": "string", "nullable": False})})

        deltas = diff_specs(old, new)

        self.assertIn("type_change", kinds(deltas))

    def test_allof_properties_are_compared_with_inline_object_type(self) -> None:
        old = spec(
            {
                "get": response(
                    {
                        "type": "object",
                        "allOf": [{"properties": {"legacy": {"type": "string"}}}],
                    }
                )
            }
        )
        new = spec({"get": response({"type": "object", "allOf": [{}]})})

        deltas = diff_specs(old, new)

        self.assertTrue(any(delta["kind"] == "property_removed" for delta in deltas))


if __name__ == "__main__":
    unittest.main()

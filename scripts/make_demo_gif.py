# -*- coding: utf-8 -*-
"""Generate a terminal-style demo GIF for README (exact text via PIL)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "demo-breaking-change.gif"
POSTER = ROOT / "assets" / "demo-poster.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 960, 540
BG = (13, 17, 23)
PANEL = (22, 27, 34)
BORDER = (48, 54, 61)
GREEN = (63, 185, 80)
RED = (248, 81, 73)
YELLOW = (210, 153, 34)
BLUE = (88, 166, 255)
MUTED = (139, 148, 158)
WHITE = (230, 237, 243)
ORANGE = (255, 166, 87)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\CascadiaMono.ttf",
        r"C:\Windows\Fonts\lucon.ttf",
        r"C:\Windows\Fonts\cour.ttf",
    ]
    if bold:
        candidates = [
            r"C:\Windows\Fonts\consolab.ttf",
            r"C:\Windows\Fonts\CascadiaMono.ttf",
        ] + candidates
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


F = font(18)
FT = font(22, bold=True)
FS = font(15)


def new_frame():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(
        [24, 24, W - 24, H - 24], radius=12, fill=PANEL, outline=BORDER, width=2
    )
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([44 + i * 22, 40, 58 + i * 22, 54], fill=c)
    d.text(
        (130, 38),
        "api-platform-skills  ·  breaking-change-review",
        font=FS,
        fill=MUTED,
    )
    return im, d


def draw_lines(d, lines, y0=78, lh=26):
    y = y0
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = item, WHITE
        d.text((48, y), text, font=F, fill=color)
        y += lh
    return y


def main() -> None:
    frames = []
    durations = []

    im, d = new_frame()
    draw_lines(
        d,
        [
            ("$ agent", MUTED),
            "",
            ("> Compare openapi.v1.yaml with openapi.v2-bad.yaml", BLUE),
            ("> Follow skills/breaking-change-review/SKILL.md", BLUE),
            ("> Give a merge verdict.", BLUE),
            "",
            ("Loading skill: breaking-change-review ...", YELLOW),
        ],
    )
    d.text((48, H - 70), "Wanbinyu/api-platform-skills", font=FS, fill=MUTED)
    frames.append(im)
    durations.append(1400)

    im, d = new_frame()
    draw_lines(
        d,
        [
            ("## Breaking change review", WHITE),
            "",
            ("Scope: shipped public API", MUTED),
            ("Diff: openapi.v1.yaml  ->  openapi.v2-bad.yaml", MUTED),
            "",
            ("Scanning deltas ........ done", GREEN),
            ("Classifying 8 changes ...", YELLOW),
        ],
    )
    frames.append(im)
    durations.append(1100)

    im, d = new_frame()
    draw_lines(
        d,
        [
            ("### Deltas", WHITE),
            "",
            ("[BREAK] listOrders auth removed", RED),
            ("[BREAK] createOrder 201 -> 200", RED),
            ("[BREAK] note became required", RED),
            ("[SEMANTIC] total_cents -> amount (dollars)", ORANGE),
            ("[BREAK] status enum rewritten", RED),
            ("[BREAK] note / customer_email removed", RED),
            ("[RISK]  internal_score oversharing", YELLOW),
        ],
    )
    frames.append(im)
    durations.append(1800)

    im, d = new_frame()
    draw_lines(
        d,
        [
            ("### Verdict", WHITE),
            "",
            ("request-changes", RED),
            "",
            ("Do not merge v2-bad.", WHITE),
            ("Keep additive evolution + deprecation window.", WHITE),
            ("Restore list auth. Keep 201 on create.", WHITE),
            ("Dual-publish money fields before unit change.", WHITE),
            "",
            ("Exit criteria: 5/5 checked", GREEN),
        ],
    )
    d.rounded_rectangle(
        [48, H - 100, 420, H - 52], radius=8, fill=(48, 20, 20), outline=RED, width=2
    )
    d.text((64, H - 88), "MERGE BLOCKED", font=FT, fill=RED)
    frames.append(im)
    durations.append(2200)

    im, d = new_frame()
    draw_lines(
        d,
        [
            ("API Platform Skills", BLUE),
            ("Design is easy. Evolution is hard.", WHITE),
            "",
            ("9 skills  |  OpenAPI evolution  |  MIT", MUTED),
            ("Claude · Codex · Cursor · Copilot", MUTED),
            "",
            ("github.com/Wanbinyu/api-platform-skills", GREEN),
        ],
    )
    frames.append(im)
    durations.append(2000)

    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )
    frames[3].save(POSTER)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"Wrote {POSTER}")


if __name__ == "__main__":
    main()

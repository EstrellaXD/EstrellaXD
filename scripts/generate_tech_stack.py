#!/usr/bin/env python3
"""Generate animated floating tech stack SVG with embedded icons."""

import base64
import urllib.request
from pathlib import Path

ICONS = [
    ("python", "python/python-original.svg", "Python"),
    ("rust", "rust/rust-original.svg", "Rust"),
    ("typescript", "typescript/typescript-original.svg", "TypeScript"),
    ("bash", "bash/bash-original.svg", "Bash"),
    ("vue", "vuejs/vuejs-original.svg", "Vue 3"),
    ("fastapi", "fastapi/fastapi-original.svg", "FastAPI"),
    ("tailwind", "tailwindcss/tailwindcss-original.svg", "Tailwind"),
    ("sqlalchemy", "sqlalchemy/sqlalchemy-original.svg", "SQLAlchemy"),
    ("postgresql", "postgresql/postgresql-original.svg", "PostgreSQL"),
    ("docker", "docker/docker-original.svg", "Docker"),
]

BASE_URL = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"

# Layout
COLS = 5
ICON_BOX = 72
ICON_SIZE = 44
GAP_X = 24
GAP_Y = 40
MARGIN_X = 16
MARGIN_Y = 16
LABEL_OFFSET = 16
FLOAT_AMPLITUDE = 8
FLOAT_DURATION = 3.0
STAGGER = 0.3


def download_icon_b64(path: str) -> str:
    url = BASE_URL + path
    response = urllib.request.urlopen(url)
    svg_bytes = response.read()
    return base64.b64encode(svg_bytes).decode("utf-8")


def generate_svg() -> str:
    rows_count = (len(ICONS) + COLS - 1) // COLS
    total_w = COLS * ICON_BOX + (COLS - 1) * GAP_X + 2 * MARGIN_X
    total_h = (
        rows_count * (ICON_BOX + LABEL_OFFSET)
        + (rows_count - 1) * (GAP_Y - LABEL_OFFSET)
        + 2 * MARGIN_Y
        + FLOAT_AMPLITUDE
    )

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
        f' width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">',
        "<style>",
        "  @keyframes float {",
        f"    0%, 100% {{ transform: translateY(0); }}",
        f"    50% {{ transform: translateY(-{FLOAT_AMPLITUDE}px); }}",
        "  }",
        f"  .f {{ animation: float {FLOAT_DURATION}s ease-in-out infinite; }}",
    ]
    for i in range(len(ICONS)):
        lines.append(f"  .d{i} {{ animation-delay: {i * STAGGER:.1f}s; }}")
    lines.extend([
        '  .lb { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;'
        " font-size: 11px; fill: #656d76; }",
        "</style>",
    ])

    icon_offset = (ICON_BOX - ICON_SIZE) // 2

    for i, (_, path, label) in enumerate(ICONS):
        col = i % COLS
        row = i // COLS
        x = MARGIN_X + col * (ICON_BOX + GAP_X)
        y = MARGIN_Y + FLOAT_AMPLITUDE + row * (ICON_BOX + GAP_Y)

        b64 = download_icon_b64(path)
        data_uri = f"data:image/svg+xml;base64,{b64}"

        lines.extend([
            f'  <g transform="translate({x},{y})">',
            f'    <g class="f d{i}">',
            f'      <rect width="{ICON_BOX}" height="{ICON_BOX}" rx="12" fill="#f6f8fa"/>',
            f'      <image href="{data_uri}" x="{icon_offset}" y="{icon_offset}" width="{ICON_SIZE}" height="{ICON_SIZE}"/>',
            f'      <text x="{ICON_BOX // 2}" y="{ICON_BOX + LABEL_OFFSET}" text-anchor="middle" class="lb">{label}</text>',
            "    </g>",
            "  </g>",
        ])

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "tech-stack-animated.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    svg = generate_svg()
    out.write_text(svg)
    print(f"Generated {out} ({len(svg):,} bytes)")

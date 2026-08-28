#!/usr/bin/env python3
"""Generate the README banner and stack strip as self-hosted animated SVGs.

Two variants per asset (dark / light) so the README can switch with
<picture media="(prefers-color-scheme: dark)">. No third-party image
services are involved: everything the profile renders lives in this repo.

    python3 assets/build_assets.py
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent

MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "ink": "#e6edf3",
        "dim": "#8b949e",
        "faint": "#6e7681",
        "line": "#2c333c",
        "accent": "#58a6ff",
    },
    "light": {
        "ink": "#1f2328",
        "dim": "#59636e",
        "faint": "#818b98",
        "line": "#d1d9e0",
        "accent": "#0969da",
    },
}

NAME = "useless007"
EYEBROW = "BANGKOK, TH"
ROTATING = [
    "go services, next.js in front, postgres underneath",
    "local models on my own gpu, not someone else's api",
    "telegram bots that run themselves on cron",
    "zig for the small sharp tools",
]

W, H = 880, 190
RADAR_CX, RADAR_CY = 772, 95
# (angle clockwise from +x, radius) -> a blip lights up as the sweep passes it
BLIPS = [(35, 30), (150, 44), (255, 18)]

STACK = [
    ("lang", ["Go", "TypeScript", "Python", "Zig", "Java"]),
    ("web", ["Next.js", "Svelte", "Astro", "Elysia", "Hono", "Bun", "FastAPI", "Fiber", "Tailwind"]),
    ("data", ["PostgreSQL", "Redis", "Neo4j", "SQLite", "Prisma"]),
    ("infra", ["Docker", "Linux", "Cloudflare Workers", "GitHub Actions", "Wails"]),
    ("ai", ["Ollama", "YOLO", "Graph RAG", "MCP"]),
]


def polar(cx, cy, angle_deg, radius):
    from math import cos, radians, sin

    a = radians(angle_deg)
    return cx + radius * cos(a), cy + radius * sin(a)


def header(theme):
    c = THEMES[theme]
    sweep_period = 8.0

    letters = "".join(
        f'<tspan class="l l{i}">{ch}</tspan>' for i, ch in enumerate(NAME)
    )

    letter_rules = "".join(
        f".l{i}{{animation-delay:{0.18 + i * 0.055:.3f}s}}" for i in range(len(NAME))
    )

    rot_texts = "".join(
        f'<text class="rot r{i}" x="66" y="163">{line}</text>'
        for i, line in enumerate(ROTATING)
    )
    rot_rules = "".join(
        f".r{i}{{animation-delay:{i * 6}s}}" for i in range(len(ROTATING))
    )

    blip_circles = ""
    blip_rules = ""
    for i, (angle, radius) in enumerate(BLIPS):
        x, y = polar(RADAR_CX, RADAR_CY, angle, radius)
        blip_circles += f'<circle class="blip b{i}" cx="{x:.2f}" cy="{y:.2f}" r="2.6"/>'
        blip_rules += f".b{i}{{animation-delay:{angle / 360 * sweep_period:.2f}s}}"

    wedge_end = polar(RADAR_CX, RADAR_CY, 58, 52)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME} — full-stack developer, Bangkok">
<title>{NAME}</title>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="{c['line']}"/>
  </pattern>
  <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.45" stop-color="#fff" stop-opacity="0.5"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0.9"/>
  </linearGradient>
  <mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#gridFade)"/></mask>
  <linearGradient id="sheenGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#fff" stop-opacity="1"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="sheen">
    <rect class="sheenbar" x="-260" y="0" width="220" height="{H}" fill="url(#sheenGrad)"/>
  </mask>
</defs>
<style>
  text{{font-family:{MONO};}}
  .panel{{fill:none;stroke:{c['line']};stroke-width:1}}
  .eyebrow{{font-size:11.5px;letter-spacing:3.6px;fill:{c['faint']};animation:fade .9s ease-out .05s backwards}}
  .dot{{fill:{c['accent']};animation:pulse 3.2s ease-in-out infinite}}
  .name{{font-size:58px;font-weight:700;letter-spacing:-2px;fill:{c['ink']}}}
  .l{{animation:fade .55s ease-out backwards}}
  {letter_rules}
  .sheentext{{font-size:58px;font-weight:700;letter-spacing:-2px;fill:{c['accent']}}}
  .sheenbar{{animation:sweepx 9s cubic-bezier(.4,0,.2,1) 1.6s infinite}}
  .rule{{stroke:{c['accent']};stroke-width:2;stroke-linecap:round;stroke-dasharray:120;animation:draw 1.1s cubic-bezier(.2,.7,.2,1) .75s backwards}}
  .caret{{fill:{c['accent']};animation:blink 2.4s steps(1) infinite}}
  .rot{{font-size:15px;fill:{c['dim']};opacity:0;animation:cycle 24s ease-in-out infinite}}
  .r0{{opacity:1}}
  {rot_rules}
  .ring{{fill:none;stroke:{c['line']};stroke-width:1}}
  .cross{{stroke:{c['line']};stroke-width:1;opacity:.7}}
  .wedge{{fill:{c['accent']};opacity:.10}}
  .spin{{transform-origin:{RADAR_CX}px {RADAR_CY}px;animation:spin {sweep_period}s linear infinite}}
  .beam{{stroke:{c['accent']};stroke-width:1.4;opacity:.75}}
  .blip{{fill:{c['accent']};opacity:0;animation:blip {sweep_period}s linear infinite}}
  {blip_rules}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
  @keyframes sweepx{{0%{{transform:translateX(0)}}45%,100%{{transform:translateX(720px)}}}}
  @keyframes draw{{from{{stroke-dashoffset:120}}to{{stroke-dashoffset:0}}}}
  @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:.15}}}}
  @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  @keyframes blip{{0%{{opacity:.95}}30%{{opacity:0}}100%{{opacity:0}}}}
  @keyframes cycle{{0%{{opacity:0}}2%{{opacity:1}}22%{{opacity:1}}25%,100%{{opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{
    .l,.eyebrow{{animation:none}}
    .sheenbar,.dot,.caret,.spin,.blip{{animation:none}}
    .rule{{animation:none}}
    .rot{{animation:none}}
  }}
</style>
<rect width="{W}" height="{H}" rx="16" fill="url(#grid)" mask="url(#gridMask)" opacity=".55"/>
<rect class="panel" x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16"/>

<circle class="dot" cx="49" cy="45" r="3"/>
<text class="eyebrow" x="62" y="49">{EYEBROW}</text>

<text class="name" x="46" y="112">{letters}</text>
<text class="sheentext" x="46" y="112" mask="url(#sheen)" aria-hidden="true">{NAME}</text>

<path class="rule" d="M48 132 H168"/>

<rect class="caret" x="48" y="151" width="2" height="16" rx="1"/>
{rot_texts}

<circle class="ring" cx="{RADAR_CX}" cy="{RADAR_CY}" r="52"/>
<circle class="ring" cx="{RADAR_CX}" cy="{RADAR_CY}" r="35" opacity=".8"/>
<circle class="ring" cx="{RADAR_CX}" cy="{RADAR_CY}" r="18" opacity=".6"/>
<line class="cross" x1="{RADAR_CX - 52}" y1="{RADAR_CY}" x2="{RADAR_CX + 52}" y2="{RADAR_CY}"/>
<line class="cross" x1="{RADAR_CX}" y1="{RADAR_CY - 52}" x2="{RADAR_CX}" y2="{RADAR_CY + 52}"/>
{blip_circles}
<g class="spin">
  <path class="wedge" d="M{RADAR_CX} {RADAR_CY} L{RADAR_CX + 52} {RADAR_CY} A52 52 0 0 1 {wedge_end[0]:.2f} {wedge_end[1]:.2f} Z"/>
  <line class="beam" x1="{RADAR_CX}" y1="{RADAR_CY}" x2="{RADAR_CX + 52}" y2="{RADAR_CY}"/>
</g>
</svg>
'''


def stack(theme):
    c = THEMES[theme]
    chip_h, chip_fs, gap, row_gap = 27, 12.5, 8, 12
    label_x, chips_x, right = 64, 84, W
    pad = 13

    rows, y = [], 8
    chips, order = [], 0
    for label, items in STACK:
        x = chips_x
        first_line_y = y
        for item in items:
            w = round(len(item) * chip_fs * 0.602 + pad * 2, 1)
            if x + w > right:
                x = chips_x
                y += chip_h + gap
            chips.append((x, y, w, item, order))
            order += 1
            x += w + gap
        rows.append((label, first_line_y))
        y += chip_h + row_gap

    height = y - row_gap + 8

    body = ""
    for label, ly in rows:
        body += (
            f'<text class="glabel" x="{label_x}" y="{ly + chip_h / 2 + 4:.1f}">{label}</text>'
        )
    for x, cy, w, item, i in chips:
        body += (
            f'<g class="chip c{i}">'
            f'<rect x="{x}" y="{cy}" width="{w}" height="{chip_h}" rx="7"/>'
            f'<text x="{x + w / 2:.1f}" y="{cy + chip_h / 2 + 4.3:.1f}">{item}</text>'
            f"</g>"
        )

    chip_rules = "".join(
        f".c{i}{{animation-delay:{0.05 + i * 0.028:.3f}s}}" for i in range(len(chips))
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img" aria-label="Tools I reach for">
<title>stack</title>
<style>
  text{{font-family:{MONO}}}
  .glabel{{font-size:11px;letter-spacing:2.4px;fill:{c['faint']};text-anchor:end}}
  .chip rect{{fill:none;stroke:{c['line']};stroke-width:1}}
  .chip text{{font-size:{chip_fs}px;fill:{c['dim']};text-anchor:middle}}
  .chip{{animation:rise .5s cubic-bezier(.2,.7,.2,1) backwards}}
  {chip_rules}
  @keyframes rise{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
  @media (prefers-reduced-motion:reduce){{.chip{{animation:none}}}}
</style>
{body}
</svg>
'''


def main():
    for theme in THEMES:
        (OUT / f"header-{theme}.svg").write_text(header(theme), encoding="utf-8")
        (OUT / f"stack-{theme}.svg").write_text(stack(theme), encoding="utf-8")
        print(f"wrote assets/header-{theme}.svg, assets/stack-{theme}.svg")


if __name__ == "__main__":
    main()

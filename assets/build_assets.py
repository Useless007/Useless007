#!/usr/bin/env python3
"""Generate the README's SVGs and the markup that shows them.

Every image the profile renders lives in this repo; no third-party image services.
Each SVG carries a light and a dark palette and picks one with prefers-color-scheme.
The script also rewrites the README blocks between <!-- gen:NAME --> markers, so the
alt text always says what the images say.

    python3 assets/build_assets.py
"""

import re
import textwrap
from html import escape
from math import cos, radians, sin
from pathlib import Path

OUT = Path(__file__).resolve().parent
README = OUT.parent / "README.md"
GH = "https://github.com/Useless007"

MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"
ADV = 0.602  # advance width of one monospace glyph, in em

THEMES = {
    "dark": {
        "ink": "#e6edf3",
        "dim": "#8b949e",
        "faint": "#7d8590",
        "line": "#2c333c",
        "accent": "#58a6ff",
        "ok": "#3fb950",
    },
    "light": {
        "ink": "#1f2328",
        "dim": "#59636e",
        "faint": "#6e7781",
        "line": "#d1d9e0",
        "accent": "#0969da",
        "ok": "#1a7f37",
    },
}
# Generators write var(--name); svg() defines both palettes, so one file serves both themes.
C = {k: f"var(--{k})" for k in THEMES["light"]}

NAME = "useless007"
EYEBROW = "THAILAND"
ROTATING = [
    "rust and react router, typed from the database up",
    "go services, next.js in front, postgres underneath",
    "local models on my own gpu, not someone else's api",
    "telegram bots that run themselves on cron",
    "zig for the small sharp tools",
]

W, H = 880, 190
RADAR_CX, RADAR_CY = 772, 95
# (angle clockwise from +x, radius) -> a blip lights up as the sweep passes it
BLIPS = [(35, 30), (150, 44), (255, 18)]

# The same field as each layer of rr-stack writes it, copied from the template.
RR_CHAIN = [
    ("postgres", "title text NOT NULL"),
    ("rust", "pub title: String"),
    ("openapi.json", '"title": {"type": "string"}'),
    ("typescript", "title: string;"),
    ("react router", "{todo.title}"),
]

WORK = [
    (
        "nebula-guard",
        "SSH honeypot. A Go agent feeds Cowrie logs to a local Gemma model and "
        "sends a Thai read of each intrusion to Telegram.",
        ["Go", "Next.js", "PostgreSQL", "Ollama", "Docker"],
    ),
    (
        "content-blueprint",
        "Windows app for content teams. It drives the Claude Code or Codex CLI "
        "you already use, re-checks every result in Go and never publishes for you.",
        ["Go", "Wails", "MCP", "GitHub Actions"],
    ),
    (
        "bun-rag-starter",
        "Graph RAG over your own documents. Redis HNSW vectors and a Neo4j graph "
        "answer together, from local embeddings, inside the sources.",
        ["Bun", "Elysia", "Neo4j", "Redis", "Svelte"],
    ),
    (
        "THESIS_FASTAPI_YOLO",
        "Thesis. An IoT parts store where a YOLO model checks each package "
        "against its order before it ships.",
        ["Python", "FastAPI", "YOLO"],
    ),
    (
        "btc-rainbow-worker",
        "Cron Worker that computes the Bitcoin power-law band from the formula, "
        "with three price sources behind a fallback chain.",
        ["TypeScript", "Cloudflare Workers", "Bun"],
    ),
    (
        "zig-typist",
        "Terminal typing trainer for Thai and English layouts. Each session "
        "appends to a JSON Lines file you can grep.",
        ["Zig"],
    ),
]

PRIVATE = [
    (
        "icefactory-app",
        "Multi-tenant plant management for an ice factory, delivered in stages. Every "
        "query scopes to the tenant and branch on the session, never to what the request "
        "sends. Every write lands in an append-only audit log, and the tests fail if "
        "either rule breaks.",
        ["Go", "Next.js", "PostgreSQL"],
    ),
    (
        "guess-my-song",
        "Guess-the-song game built from the player's own Spotify library. Hono on "
        "Cloudflare Workers, one Durable Object per session, and one hostname for both "
        "apps, so the cookie stays first-party and there is no CORS.",
        ["TypeScript", "Hono", "Durable Objects", "Astro"],
    ),
    (
        "pea-calculator-backup",
        "Electricity-meter tracker. The app encrypts the database before it leaves the "
        "machine, the key never enters Git or the image, and the scheduler runs the "
        "backups it missed.",
        ["Node.js", "Docker"],
    ),
]

STACK = [
    ("lang", ["Go", "Rust", "TypeScript", "Python", "Zig", "Java"]),
    ("web", ["React Router", "Next.js", "Svelte", "Astro", "Axum", "Elysia", "Hono", "Bun", "FastAPI", "Fiber", "Tailwind"]),
    ("data", ["PostgreSQL", "SQLx", "Redis", "Neo4j", "SQLite", "Prisma"]),
    ("infra", ["Docker", "Linux", "Cloudflare Workers", "Vercel", "GitHub Actions", "Wails"]),
    ("ai", ["Ollama", "YOLO", "Graph RAG", "MCP"]),
]


def text_w(s, fs):
    return len(s) * fs * ADV


def polar(cx, cy, angle_deg, radius):
    a = radians(angle_deg)
    return cx + radius * cos(a), cy + radius * sin(a)


def palette(theme):
    return ";".join(f"--{k}:{v}" for k, v in THEMES[theme].items())


def svg(w, h, label, style, body):
    # An SVG inside <img> takes prefers-color-scheme from the color-scheme of the page
    # around it (Chrome, Firefox), and GitHub sets that from the reader's theme.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{escape(label)}">\n'
        f"<title>{escape(label)}</title>\n<style>\n"
        f"  svg{{{palette('light')}}}\n"
        f"  @media (prefers-color-scheme:dark){{svg{{{palette('dark')}}}}}\n"
        f"  text{{font-family:{MONO}}}\n{style}\n</style>\n"
        f"{body}\n</svg>\n"
    )


def dot_grid(c, w, h):
    """The faded dot grid behind the header and the rr-stack card."""
    return f'''<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" style="fill:{c['line']}"/>
  </pattern>
  <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.45" stop-color="#fff" stop-opacity="0.5"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0.9"/>
  </linearGradient>
  <mask id="gridMask"><rect width="{w}" height="{h}" fill="url(#gridFade)"/></mask>
</defs>
<rect width="{w}" height="{h}" rx="16" fill="url(#grid)" mask="url(#gridMask)" opacity=".55"/>'''


def chips(items, x, y, fs=10.5, h=20, pad=8, gap=6, align="left", right=None):
    """Outlined tags in one row. Returns (svg, total width)."""
    widths = [text_w(s, fs) + pad * 2 for s in items]
    total = sum(widths) + gap * (len(items) - 1)
    if align == "right":
        x = right - total
    out = ""
    for s, w in zip(items, widths):
        out += (
            f'<rect class="chip" x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="5"/>'
            f'<text class="chipt" x="{x + w / 2:.1f}" y="{y + h / 2 + fs * 0.36:.1f}">{escape(s)}</text>'
        )
        x += w + gap
    return out, total


def chip_style(c, fs=10.5):
    return (
        f"  .chip{{fill:none;stroke:{c['line']};stroke-width:1}}\n"
        f"  .chipt{{font-size:{fs}px;fill:{c['faint']};text-anchor:middle}}"
    )


def header():
    c = C
    sweep_period = 8.0
    slot = 6  # seconds each rotating line stays up
    cycle = slot * len(ROTATING)
    share = 100 / len(ROTATING)

    letters = "".join(f'<tspan class="l l{i}">{ch}</tspan>' for i, ch in enumerate(NAME))
    letter_rules = "".join(
        f".l{i}{{animation-delay:{0.18 + i * 0.055:.3f}s}}" for i in range(len(NAME))
    )
    rot_texts = "".join(
        f'<text class="rot r{i}" x="66" y="163">{escape(line)}</text>'
        for i, line in enumerate(ROTATING)
    )
    rot_rules = "".join(f".r{i}{{animation-delay:{i * slot}s}}" for i in range(len(ROTATING)))

    blip_circles = ""
    blip_rules = ""
    for i, (angle, radius) in enumerate(BLIPS):
        x, y = polar(RADAR_CX, RADAR_CY, angle, radius)
        blip_circles += f'<circle class="blip b{i}" cx="{x:.2f}" cy="{y:.2f}" r="2.6"/>'
        blip_rules += f".b{i}{{animation-delay:{angle / 360 * sweep_period:.2f}s}}"

    wedge_end = polar(RADAR_CX, RADAR_CY, 58, 52)

    style = f'''  .panel{{fill:none;stroke:{c['line']};stroke-width:1}}
  .eyebrow{{font-size:11.5px;letter-spacing:3.6px;fill:{c['faint']};animation:fade .9s ease-out .05s backwards}}
  .dot{{fill:{c['accent']};animation:pulse 3.2s ease-in-out infinite}}
  .name{{font-size:58px;font-weight:700;letter-spacing:-2px;fill:{c['ink']}}}
  .l{{animation:fade .55s ease-out backwards}}
  {letter_rules}
  .sheentext{{font-size:58px;font-weight:700;letter-spacing:-2px;fill:{c['accent']}}}
  .sheenbar{{animation:sweepx 9s cubic-bezier(.4,0,.2,1) 1.6s infinite}}
  .rule{{stroke:{c['accent']};stroke-width:2;stroke-linecap:round;stroke-dasharray:120;animation:draw 1.1s cubic-bezier(.2,.7,.2,1) .75s backwards}}
  .caret{{fill:{c['accent']};animation:blink 2.4s steps(1) infinite}}
  .rot{{font-size:15px;fill:{c['dim']};opacity:0;animation:cycle {cycle}s ease-in-out infinite}}
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
  @keyframes cycle{{0%{{opacity:0}}{share * 0.08:.2f}%{{opacity:1}}{share * 0.88:.2f}%{{opacity:1}}{share:.2f}%,100%{{opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{
    .l,.eyebrow,.sheenbar,.dot,.caret,.spin,.blip,.rule,.rot{{animation:none}}
  }}'''

    body = f'''{dot_grid(c, W, H)}
<defs>
  <linearGradient id="sheenGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#fff" stop-opacity="1"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="sheen">
    <rect class="sheenbar" x="-260" y="0" width="220" height="{H}" fill="url(#sheenGrad)"/>
  </mask>
</defs>
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
</g>'''
    return svg(W, H, f"{NAME}, full-stack developer in Thailand", style, body)


def lit(name, t, period, off, on, hold_until, fade=0.3):
    """Keyframes that switch from `off` to `on` at second t and back after hold_until."""
    p = lambda s: f"{s / period * 100:.2f}%"
    return (
        f"@keyframes {name}{{0%,{p(t)}{{{off}}}{p(t + fade)},{p(hold_until)}{{{on}}}"
        f"{p(hold_until + fade * 2)},100%{{{off}}}}}"
    )


def rr_stack():
    """The one animated moment below the header: a field lights up layer by layer."""
    c = C
    w, h, x0 = W, 268, 36
    period, step, hold = 9.0, 0.7, 7.8
    fs, pad, box_h, box_y = 11, 10, 32, 166

    widths = [text_w(code, fs) + pad * 2 for _, code in RR_CHAIN]
    gap = (w - 2 * x0 - sum(widths)) / (len(RR_CHAIN) - 1)
    assert gap >= 24, f"rr-stack chain is too wide: {gap:.1f}px between boxes"

    style = [
        f"  .panel{{fill:none;stroke:{c['accent']};stroke-opacity:.45;stroke-width:1}}",
        f"  .title{{font-size:40px;font-weight:700;letter-spacing:-1.5px;fill:{c['ink']}}}",
        f"  .tag{{font-size:14px;fill:{c['dim']}}}",
        f"  .layer{{font-size:10.5px;fill:{c['faint']}}}",
        # Base styles are the finished state, so reduced motion shows the whole chain.
        f"  .box{{fill:{c['accent']};fill-opacity:.08;stroke:{c['accent']};stroke-width:1}}",
        f"  .code{{font-size:{fs}px;fill:{c['ink']}}}",
        f"  .link{{fill:none;stroke:{c['accent']};stroke-width:1.2;stroke-linecap:round;stroke-linejoin:round}}",
        f"  .cmd{{font-size:13px;fill:{c['dim']}}}",
        f"  .exit{{font-size:13px;font-weight:700;fill:{c['ok']}}}",
        f"  .why{{font-size:13px;fill:{c['faint']}}}",
    ]
    keyframes, body = [], [dot_grid(c, w, h)]
    body.append(f'<rect class="panel" x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16"/>')
    body.append(f'<text class="title" x="{x0}" y="78">rr-stack</text>')
    body.append(
        f'<text class="tag" x="{x0 + 2}" y="110">React Router + Rust (Axum), '
        "typed from the database to the screen.</text>"
    )

    x, mid = x0, box_y + box_h / 2
    for i, ((layer, code), bw) in enumerate(zip(RR_CHAIN, widths)):
        t = 0.5 + i * step
        body.append(f'<text class="layer" x="{x:.1f}" y="{box_y - 9}">{layer}</text>')
        body.append(
            f'<rect class="box b{i}" x="{x:.1f}" y="{box_y}" width="{bw:.1f}" height="{box_h}" rx="6"/>'
            f'<text class="code k{i}" x="{x + pad:.1f}" y="{mid + fs * 0.36:.1f}">{escape(code)}</text>'
        )
        style.append(f"  .b{i}{{animation:b{i} {period}s linear infinite}}")
        style.append(f"  .k{i}{{animation:k{i} {period}s linear infinite}}")
        keyframes.append(lit(f"b{i}", t, period, f"fill-opacity:0;stroke:{c['line']}", f"fill-opacity:.08;stroke:{c['accent']}", hold))
        keyframes.append(lit(f"k{i}", t, period, f"fill:{c['faint']}", f"fill:{c['ink']}", hold))
        if i < len(RR_CHAIN) - 1:
            x1, x2 = x + bw + 5, x + bw + gap - 5
            length = (x2 - x1) + 2 * (4**2 + 4**2) ** 0.5
            body.append(
                f'<path class="link a{i}" d="M{x1:.1f} {mid} H{x2:.1f} m-4 -4 l4 4 l-4 4" '
                f'stroke-dasharray="{length:.1f}"/>'
            )
            style.append(f"  .a{i}{{animation:a{i} {period}s linear infinite}}")
            keyframes.append(lit(f"a{i}", t + 0.2, period, f"stroke-dashoffset:{length:.1f}", "stroke-dashoffset:0", hold, fade=0.4))
        x += bw + gap

    done = 0.5 + len(RR_CHAIN) * step
    cmd = "$ bun run check"
    exit_x = x0 + text_w(cmd, 13) + 18
    why_x = exit_x + text_w("exit 0", 13) + 14
    body.append(f'<text class="cmd" x="{x0}" y="236">{cmd}</text>')
    body.append(f'<text class="exit res" x="{exit_x:.1f}" y="236">exit 0</text>')
    body.append(
        f'<text class="why res" x="{why_x:.1f}" y="236">'
        "the SQL, the API, the contract and the UI agree</text>"
    )
    style.append(f"  .res{{animation:res {period}s linear infinite}}")
    keyframes.append(lit("res", done, period, "opacity:0", "opacity:1", hold))

    style += [f"  {k}" for k in keyframes]
    style.append("  @media (prefers-reduced-motion:reduce){.box,.code,.link,.res{animation:none}}")
    label = "rr-stack: React Router + Rust (Axum), typed from the database to the screen"
    return svg(w, h, label, "\n".join(style), "\n".join(body))


CARD_W, CARD_H, CARD_PAD = 436, 158, 22
CARD_FS, CARD_LINES = 12, 3


def card(name, desc, tags):
    c = C
    per_line = int((CARD_W - CARD_PAD * 2) / (CARD_FS * ADV))
    lines = textwrap.wrap(desc, per_line)
    assert len(lines) <= CARD_LINES, f"{name}: description wraps to {len(lines)} lines"
    tag_svg, tag_w = chips(tags, CARD_PAD, CARD_H - CARD_PAD - 20)
    assert tag_w <= CARD_W - CARD_PAD * 2, f"{name}: tags overflow the card"

    style = "\n".join([
        f"  .panel{{fill:none;stroke:{c['line']};stroke-width:1}}",
        f"  .name{{font-size:15px;font-weight:700;fill:{c['ink']}}}",
        f"  .desc{{font-size:{CARD_FS}px;fill:{c['dim']}}}",
        chip_style(c),
    ])
    desc_svg = "".join(
        f'<text class="desc" x="{CARD_PAD}" y="{66 + i * 18}">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    body = (
        f'<rect class="panel" x=".5" y=".5" width="{CARD_W - 1}" height="{CARD_H - 1}" rx="12"/>\n'
        f'<text class="name" x="{CARD_PAD}" y="38">{escape(name)}</text>\n{desc_svg}\n{tag_svg}'
    )
    return svg(CARD_W, CARD_H, f"{name}: {desc}", style, body)


def private_panel():
    c = C
    x0, fs, lh, top = 36, 12, 18, 22
    per_line = int((W - x0 * 2) / (fs * ADV))
    rows, y = [], top
    for name, desc, tags in PRIVATE:
        lines = textwrap.wrap(desc, per_line)
        assert len(lines) <= 3, f"{name}: description wraps to {len(lines)} lines"
        rows.append((y, name, lines, tags))
        y += 34 + len(lines) * lh + 16
    h = y - 16 + top

    style = "\n".join([
        f"  .panel{{fill:none;stroke:{c['line']};stroke-width:1}}",
        f"  .sep{{stroke:{c['line']};stroke-width:1}}",
        f"  .lock{{fill:none;stroke:{c['faint']};stroke-width:1.3;stroke-linejoin:round}}",
        f"  .name{{font-size:15px;font-weight:700;fill:{c['ink']}}}",
        f"  .desc{{font-size:{fs}px;fill:{c['dim']}}}",
        chip_style(c),
    ])
    body = [f'<rect class="panel" x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="16"/>']
    for i, (ry, name, lines, tags) in enumerate(rows):
        if i:
            body.append(f'<line class="sep" x1="{x0}" y1="{ry - 8}" x2="{W - x0}" y2="{ry - 8}"/>')
        base = ry + 22
        # A padlock drawn in place, so it does not depend on an emoji font.
        body.append(
            f'<path class="lock" d="M{x0 + 1} {base - 7} h10 v8 h-10 z '
            f'M{x0 + 3} {base - 7} v-3 a3 3 0 0 1 6 0 v3"/>'
        )
        body.append(f'<text class="name" x="{x0 + 20}" y="{base}">{escape(name)}</text>')
        tag_svg, _ = chips(tags, 0, base - 14, align="right", right=W - x0)
        body.append(tag_svg)
        for j, line in enumerate(lines):
            body.append(f'<text class="desc" x="{x0}" y="{base + 24 + j * lh}">{escape(line)}</text>')
    label = "Private work: " + " ".join(f"{n}: {d}" for n, d, _ in PRIVATE)
    return svg(W, h, label, style, "\n".join(body))


def stack():
    c = C
    chip_h, chip_fs, gap, row_gap = 27, 12.5, 8, 12
    label_x, chips_x, right = 64, 84, W
    pad = 13

    rows, y = [], 8
    placed, order = [], 0
    for label, items in STACK:
        x = chips_x
        first_line_y = y
        for item in items:
            w = round(text_w(item, chip_fs) + pad * 2, 1)
            if x + w > right:
                x = chips_x
                y += chip_h + gap
            placed.append((x, y, w, item, order))
            order += 1
            x += w + gap
        rows.append((label, first_line_y))
        y += chip_h + row_gap

    height = y - row_gap + 8

    body = ""
    for label, ly in rows:
        body += f'<text class="glabel" x="{label_x}" y="{ly + chip_h / 2 + 4:.1f}">{label}</text>'
    for x, cy, w, item, i in placed:
        body += (
            f'<g class="chip c{i}">'
            f'<rect x="{x}" y="{cy}" width="{w}" height="{chip_h}" rx="7"/>'
            f'<text x="{x + w / 2:.1f}" y="{cy + chip_h / 2 + 4.3:.1f}">{escape(item)}</text>'
            f"</g>"
        )

    chip_rules = "".join(f".c{i}{{animation-delay:{0.05 + i * 0.028:.3f}s}}" for i in range(len(placed)))
    style = f'''  .glabel{{font-size:11px;letter-spacing:2.4px;fill:{c['faint']};text-anchor:end}}
  .chip rect{{fill:none;stroke:{c['line']};stroke-width:1}}
  .chip text{{font-size:{chip_fs}px;fill:{c['dim']};text-anchor:middle}}
  .chip{{animation:rise .5s cubic-bezier(.2,.7,.2,1) backwards}}
  {chip_rules}
  @keyframes rise{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
  @media (prefers-reduced-motion:reduce){{.chip{{animation:none}}}}'''
    return svg(W, height, "Tools I reach for", style, body)


def image(stem, alt, width=None, href=None):
    # A plain <img>, not <picture>: GitHub splits <a><picture> apart, and the image then
    # links to the SVG file instead of href. The SVG switches theme by itself.
    size = f' width="{width}"' if width else ""
    alt = escape(alt, quote=False).replace('"', "&quot;")
    img = f'<img src="assets/{stem}.svg"{size} alt="{alt}">'
    return f'<a href="{href}">{img}</a>' if href else img


def readme_blocks():
    work = "\n".join(
        image(f"card-{name}", f"{name}: {desc} ({', '.join(tags)})", "49%", f"{GH}/{name}")
        for name, desc, tags in WORK
    )
    private = image(
        "private",
        " ".join(f"{n}: {d} ({', '.join(t)})." for n, d, t in PRIVATE),
    )
    tools = image("stack", "; ".join(", ".join(items) for _, items in STACK))
    rr = image(
        "rr-stack",
        "rr-stack: React Router + Rust (Axum), typed from the database to the screen. The same "
        "title field lights up in " + ", ".join(layer for layer, _ in RR_CHAIN)
        + ", then bun run check exits 0.",
        href=f"{GH}/rr-stack",
    )
    header_img = image("header", f"{NAME}, full-stack developer in Thailand")
    return {"header": header_img, "rr": rr, "work": f"<p>\n{work}\n</p>", "private": private, "tools": tools}


def write_readme():
    text = README.read_text(encoding="utf-8")
    for key, block in readme_blocks().items():
        pattern = re.compile(rf"(<!-- gen:{key} -->).*?(<!-- /gen:{key} -->)", re.S)
        text, n = pattern.subn(lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}", text)
        assert n == 1, f"README needs exactly one <!-- gen:{key} --> block, found {n}"
    README.write_text(text, encoding="utf-8")


def main():
    files = {
        "header": header(),
        "rr-stack": rr_stack(),
        "private": private_panel(),
        "stack": stack(),
    }
    for name, desc, tags in WORK:
        files[f"card-{name}"] = card(name, desc, tags)
    for stem, content in files.items():
        (OUT / f"{stem}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} svgs")
    write_readme()
    print("updated README.md blocks")


if __name__ == "__main__":
    main()

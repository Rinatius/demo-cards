"""Generate one 16:9 illustration per Starshield card: python3 tools/starshield_illustrations.py cards/starshield/img"""
import os, random, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
W, H = 640, 360
GOLD, LIGHT, RED, BLUE, YEL, DIM = "#f2b84b", "#e8eef5", "#e05a47", "#3a7bd5", "#f5d33a", "#7f93ab"


def frame(seed, body, earth=True):
    r = random.Random(seed)
    stars = "".join(
        f'<circle cx="{r.randint(0, W)}" cy="{r.randint(0, H)}" r="{r.choice([0.6, 0.9, 1.3])}" fill="#fff" opacity="{r.uniform(.3, .9):.2f}"/>'
        for _ in range(70))
    earth_svg = ('<ellipse cx="320" cy="560" rx="520" ry="250" fill="url(#earth)"/>'
                 '<ellipse cx="320" cy="560" rx="520" ry="250" fill="none" stroke="#6fb3ff" stroke-opacity=".5" stroke-width="3"/>') if earth else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1626"/><stop offset="1" stop-color="#1b3556"/></linearGradient>
<radialGradient id="earth" cx=".5" cy=".2" r=".8"><stop offset="0" stop-color="#2f6fa8"/><stop offset="1" stop-color="#0f2f52"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}{earth_svg}
<g font-family="system-ui, -apple-system, Segoe UI, sans-serif">{body}</g>
</svg>'''


def sat(x, y, s=1.0, color=LIGHT):
    """A Starlink-style flat satellite with one long solar array."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-22" y="-8" width="44" height="16" rx="2" fill="{color}"/>'
            f'<rect x="22" y="-2" width="10" height="4" fill="{DIM}"/>'
            f'<rect x="32" y="-14" width="70" height="28" fill="#2a5d9c" stroke="{LIGHT}" stroke-width="1.5"/>'
            f'<path d="M49 -14v28M67 -14v28M84 -14v28" stroke="{LIGHT}" stroke-opacity=".5"/></g>')


def label(text, x=320, y=300, size=34, color=GOLD, weight=800):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="{weight}" fill="{color}">{text}</text>'


def shield(x, y, s=1.0, fill=GOLD):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -50 L42 -36 V2 C42 30 20 46 0 56 C-20 46 -42 30 -42 2 V-36 Z" '
            f'fill="{fill}" stroke="#0b1626" stroke-width="3"/></g>')


def doc(x, y, w=170, h=210):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{LIGHT}"/>'


def lines(x, y, n, w=120, gap=20, color="#b9c4d1"):
    return "".join(f'<rect x="{x}" y="{y + i * gap}" width="{w - (i % 3) * 18}" height="7" rx="3" fill="{color}"/>' for i in range(n))


def drone(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-60 0 L40 -6 L60 0 L40 6 Z" fill="{LIGHT}"/>'
            f'<path d="M-10 -3 L-30 -40 L-18 -40 L10 -3 Z M-10 3 L-30 40 L-18 40 L10 3 Z" fill="{DIM}"/>'
            f'<path d="M-55 -2 L-70 -18 L-62 -18 L-48 -2 Z M-55 2 L-70 18 L-62 18 L-48 2 Z" fill="{DIM}"/></g>')


ART = {}

ART["what-is-starshield"] = frame(1,
    sat(270, 150, 1.6) + shield(220, 150, .42) +
    f'<path d="M226 168 L120 300 M226 168 L340 300" stroke="{GOLD}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6"/>')

ART["who-controls-it"] = frame(2,
    shield(320, 160, 1.9, "#c43c32") +
    "".join(f'<path transform="translate({cx} {cy}) scale(.9)" d="M0 -12 L3.5 -4 L12 -4 L5 1.5 L7.5 10 L0 5 L-7.5 10 L-5 1.5 L-12 -4 L-3.5 -4 Z" fill="{LIGHT}"/>'
            for cx, cy in [(290, 135), (320, 125), (350, 135)]) +
    f'<rect x="270" y="160" width="100" height="14" rx="3" fill="{LIGHT}"/><rect x="270" y="184" width="100" height="14" rx="3" fill="{LIGHT}"/>' +
    f'<text x="120" y="150" font-size="140" font-weight="900" fill="{GOLD}" font-family="Georgia, serif">“</text>'
    f'<text x="450" y="230" font-size="140" font-weight="900" fill="{GOLD}" font-family="Georgia, serif">”</text>', earth=False)

swarm = [(90, 70), (190, 110), (300, 60), (410, 105), (520, 65), (140, 170), (360, 160), (560, 150), (250, 200)]
ART["nro-spy-network"] = frame(3,
    "".join(f'<path d="M{x} {y + 8} L{x - 26} 330 L{x + 26} 330 Z" fill="{GOLD}" opacity=".10"/>' for x, y in swarm) +
    "".join(sat(x - 20, y, .45) for x, y in swarm))

ART["first-nro-launch"] = frame(4,
    f'<path d="M200 360 C260 300 300 220 330 120" stroke="#ffffff" stroke-opacity=".25" stroke-width="18" fill="none" stroke-linecap="round"/>'
    f'<g transform="translate(345 85) rotate(22)">'
    f'<path d="M0 -60 C10 -45 12 -30 12 -20 V70 H-12 V-20 C-12 -30 -10 -45 0 -60 Z" fill="{LIGHT}"/>'
    f'<rect x="-12" y="20" width="24" height="6" fill="#0b1626"/>'
    f'<path d="M-12 70 L-24 92 L-12 84 Z M12 70 L24 92 L12 84 Z" fill="{DIM}"/>'
    f'<path d="M-9 72 Q0 140 9 72 Z" fill="{GOLD}"/><path d="M-5 72 Q0 110 5 72 Z" fill="#fff6d0"/></g>' +
    label("NROL-146 · MAY 22, 2024", 470, 320, 22, LIGHT, 700))

ART["how-many-satellites"] = frame(5,
    f'<circle cx="230" cy="185" r="95" fill="url(#earth)" stroke="#6fb3ff" stroke-opacity=".5" stroke-width="3"/>' +
    "".join(f'<ellipse cx="230" cy="185" rx="{140 + i * 12}" ry="{50 + i * 10}" transform="rotate({a} 230 185)" fill="none" stroke="{DIM}" stroke-opacity=".6"/>'
            for i, a in enumerate([-20, 15, 50])) +
    "".join(f'<circle cx="{230 + (140 + (k % 3) * 12) * c:.1f}" cy="{185 + (50 + (k % 3) * 10) * s:.1f}" r="3.5" fill="{GOLD}" transform="rotate({[-20, 15, 50][k % 3]} 230 185)"/>'
            for k, (c, s) in enumerate([(__import__("math").cos(t / 4.0), __import__("math").sin(t / 4.0)) for t in range(25)])) +
    label("~249", 490, 200, 64) + label("satellites, by one tracker's count", 490, 235, 16, LIGHT, 500), earth=False)

ART["first-space-force-deal"] = frame(6,
    doc(230, 50) + lines(255, 80, 7) +
    f'<g transform="rotate(-12 380 230)"><rect x="300" y="195" width="170" height="70" rx="8" fill="none" stroke="{RED}" stroke-width="6"/>' +
    label("$70M", 385, 245, 42, RED) + '</g>', earth=False)

ART["golden-dome-awards"] = frame(7,
    f'<path d="M80 330 A240 240 0 0 1 560 330" fill="{GOLD}" fill-opacity=".12" stroke="{GOLD}" stroke-width="4"/>'
    f'<path d="M160 330 A160 160 0 0 1 480 330" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="8 8"/>' +
    "".join(sat(x, y, .35) for x, y in [(120, 200), (230, 112), (370, 100), (480, 160)]) +
    label("$6.45B", 320, 250, 58))

nodes = [(90, 90), (220, 60), (360, 95), (500, 60), (160, 180), (300, 190), (440, 175), (560, 170)]
edges = [(0, 1), (1, 2), (2, 3), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6), (3, 6), (3, 7), (4, 5), (5, 6), (6, 7)]
ART["data-network-backbone"] = frame(8,
    "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{GOLD}" stroke-width="2" stroke-opacity=".8"/>' for a, b in edges) +
    "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{LIGHT}" stroke="{GOLD}" stroke-width="3"/>' for x, y in nodes))

ART["ukraine-terminals"] = frame(9,
    f'<rect x="0" y="0" width="{W}" height="180" fill="#1f4f8f"/><rect x="0" y="180" width="{W}" height="180" fill="#d9ad1f"/>'
    f'<g transform="translate(230 210) rotate(-25)"><rect x="-80" y="-45" width="160" height="90" rx="10" fill="{LIGHT}"/>'
    f'<rect x="-70" y="-35" width="140" height="70" rx="6" fill="#c9d3de"/></g>'
    f'<rect x="222" y="240" width="16" height="80" fill="{DIM}"/><rect x="190" y="316" width="80" height="10" rx="4" fill="{DIM}"/>' +
    "".join(f'<path d="M{300 + i * 22} {120 - i * 10} a{40 + i * 22} {40 + i * 22} 0 0 1 {30 + i * 14} {50 + i * 10}" fill="none" stroke="{LIGHT}" stroke-width="5" stroke-linecap="round" opacity="{1 - i * .25}"/>' for i in range(3)) +
    label("×3,000", 500, 250, 56, LIGHT), earth=False)

ART["ukraine-speed-cap"] = frame(10,
    drone(200, 130, 1.3) +
    "".join(f'<line x1="{60 - i * 10}" y1="{110 + i * 20}" x2="{110 - i * 10}" y2="{110 + i * 20}" stroke="{LIGHT}" stroke-opacity=".5" stroke-width="4" stroke-linecap="round"/>' for i in range(3)) +
    f'<path d="M380 250 A90 90 0 0 1 560 250" fill="none" stroke="{DIM}" stroke-width="14"/>'
    f'<path d="M380 250 A90 90 0 0 1 532 186" fill="none" stroke="{RED}" stroke-width="14"/>'
    f'<line x1="470" y1="250" x2="535" y2="195" stroke="{LIGHT}" stroke-width="6" stroke-linecap="round"/><circle cx="470" cy="250" r="10" fill="{LIGHT}"/>' +
    label("100 mph", 470, 300, 26, LIGHT) +
    f'<g stroke="{RED}" stroke-width="8" stroke-linecap="round"><line x1="300" y1="70" x2="340" y2="110"/><line x1="340" y1="70" x2="300" y2="110"/></g>', earth=False)


def bubble(x, y, w, h, text, fill):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}"/>'
            f'<path d="M{x + 30} {y + h} l10 22 l14 -22 Z" fill="{fill}"/>' + label(text, x + w / 2, y + h / 2 + 9, 24, "#0b1626", 800))


ART["who-ordered-cap"] = frame(11,
    bubble(50, 70, 160, 64, "MUSK", LIGHT) + bubble(240, 140, 170, 64, "REUTERS", GOLD) + bubble(440, 60, 150, 64, "RUBIO", LIGHT) +
    label("?", 320, 110, 90, LIGHT, 900), earth=False)

ART["ukraine-access-now"] = frame(12,
    f'<rect x="0" y="0" width="{W}" height="180" fill="#1f4f8f"/><rect x="0" y="180" width="{W}" height="180" fill="#d9ad1f"/>' +
    "".join(f'<rect x="{220 + i * 50}" y="{250 - (i + 1) * 40}" width="34" height="{(i + 1) * 40}" rx="4" fill="{LIGHT}" opacity=".35"/>' for i in range(4)) +
    f'<line x1="200" y1="270" x2="440" y2="70" stroke="{RED}" stroke-width="14" stroke-linecap="round"/>' +
    label("OFFLINE", 320, 320, 34, LIGHT), earth=False)

ART["conflict-of-interest"] = frame(13,
    f'<rect x="314" y="80" width="12" height="220" fill="{LIGHT}"/><rect x="260" y="296" width="120" height="14" rx="5" fill="{LIGHT}"/>'
    f'<g transform="rotate(-10 320 90)"><rect x="150" y="84" width="340" height="10" rx="4" fill="{LIGHT}"/>'
    f'<path d="M170 94 L140 190 M170 94 L200 190 M470 94 L440 190 M470 94 L500 190" stroke="{DIM}" stroke-width="2"/>'
    f'<path d="M130 190 H210 A40 22 0 0 1 130 190 Z" fill="{GOLD}"/><path d="M430 190 H510 A40 22 0 0 1 430 190 Z" fill="{LIGHT}"/>' +
    label("$", 170, 180, 42, GOLD) +
    f'<path d="M445 186 A25 25 0 0 1 495 186 Z" fill="{LIGHT}"/><rect x="467" y="148" width="6" height="14" fill="{LIGHT}"/></g>', earth=False)

ART["secrecy"] = frame(14,
    doc(200, 40, 240, 290) +
    "".join(f'<rect x="225" y="{90 + i * 26}" width="{190 - (i % 4) * 30}" height="12" rx="2" fill="{"#0b1626" if i % 3 != 1 else "#b9c4d1"}"/>' for i in range(8)) +
    f'<g transform="rotate(-14 320 190)"><rect x="200" y="160" width="240" height="56" rx="6" fill="none" stroke="{RED}" stroke-width="5"/>' +
    label("CLASSIFIED", 320, 199, 32, RED) + '</g>', earth=False)

for k, svg in ART.items():
    with open(os.path.join(out, f"{k}.svg"), "w") as f:
        f.write(svg)
print(len(ART), "svgs")

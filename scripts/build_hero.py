#!/usr/bin/env python3
"""Draw the Düsseldorf skyline hero from the public GitHub contribution calendar.

Each building is one week. If the calendar cannot be read, existing art stays.
"""
import html.parser
import math
import pathlib
import random
import re
import sys
import urllib.error
import urllib.request

USER = "amermmohammed"
URL = f"https://github.com/users/{USER}/contributions"
W, H, HORIZON = 1280, 600, 470

PALETTES = {
    "dark": dict(
        sky=["#050816", "#0d1038", "#2a1659", "#6b2a7d", "#d9536f"], star="#ffffff", star_op=1,
        moon="#fff4d6", aurora=["#2ee6a6", "#5b6cff", "#d04dff"], far="#1c1647", mid_a="#17153a", mid_b="#0a0b20",
        rim="#6f5bd0", win=["#39d353", "#26a641", "#ffd27a"], water_a="#1b1140", water_b="#04050f",
        fg="#ffffff", muted="#c9c6e8", tower="#c5c8e6", tower_dark="#34345f", arch="#07081a", glow="#ff4d6d",
    ),
    "light": dict(
        sky=["#29396f", "#5a5da3", "#b079ab", "#f49b82", "#ffdca3"], star="#ffffff", star_op=.55,
        moon="#fff8e7", aurora=["#ffd0a6", "#ffb3c1", "#c8b6ff"], far="#7a6fa8", mid_a="#463f7d", mid_b="#231f4d",
        rim="#ffc58f", win=["#ffe29a", "#ffc875", "#b6f5c3"], water_a="#c98a9b", water_b="#2e2a60",
        fg="#ffffff", muted="#fff0e0", tower="#f4e6e6", tower_dark="#4c4580", arch="#1b1840", glow="#ff4d6d",
    ),
}


class CalendarError(Exception):
    pass


class _Calendar(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attrs):
        if tag != "td":
            return
        data = dict(attrs)
        date, level = data.get("data-date"), data.get("data-level")
        if date and level in {"0", "1", "2", "3", "4"} and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            self.days.append((date, int(level)))


def parse_weeks(page):
    parser = _Calendar()
    parser.feed(page)
    days = sorted(set(parser.days))
    if len(days) < 300:
        raise CalendarError(f"only {len(days)} days found")
    return [
        {"start": days[i][0], "score": sum(level for _, level in days[i : i + 7])}
        for i in range(0, len(days), 7)
    ]


def fetch_weeks():
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return parse_weeks(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as error:
        raise CalendarError(str(error)) from error


def rect_path(items):
    return "".join(f"M{x} {y}h{w}v{h}h-{w}z" for x, y, w, h in items)


def buildings(weeks):
    peak = max(max(week["score"] for week in weeks), 1)
    width = W / len(weeks)
    result = []
    for index, week in enumerate(weeks):
        score = week["score"]
        rng = random.Random(week["start"])
        x = round(index * width, 1)
        left_side = x < 880
        limit = 205 if left_side else 285
        height = 34 + (limit - 34) * math.sqrt(score / peak) + rng.uniform(-5, 9)
        result.append(dict(x=x, w=round(width + .6, 1), h=round(max(26, min(limit, height))), score=score / peak, rng=rng))
    return result


def crane(block):
    x = round(block["x"] + block["w"] / 2, 1)
    top = HORIZON - block["h"]
    mast = top - 58
    return (
        f'<g fill="none" stroke="#f5b83d" stroke-width="2" stroke-linecap="round">'
        f'<path d="M{x} {top}V{mast}M{x - 66} {mast + 5}H{x + 9}M{x} {mast - 8}L{x - 48} {mast + 5}M{x} {mast - 8}L{x + 9} {mast + 5}"/>'
        f'<g class="hook"><path stroke-width="1.2" d="M{x - 44} {mast + 5}v22"/><rect x="{x - 49}" y="{mast + 27}" width="10" height="6" fill="#f5b83d" stroke="none"/></g>'
        f'</g><circle class="beacon" cx="{x}" cy="{mast - 9}" r="2.6" fill="#ff4d6d"/>'
    )


def city(weeks, p):
    blocks = buildings(weeks)
    body, rims, antennas = [], [], []
    windows = [[] for _ in range(6)]
    count = 0
    for block in blocks:
        rng = block["rng"]
        x, w, h = block["x"], block["w"], block["h"]
        top = HORIZON - h
        body.append((x, top, w, h))
        rims.append((x, top, w, 1.4))
        roll = rng.random()
        if roll < .16 and h > 80:
            body.append((round(x + w * .25, 1), top - 9, round(w * .5, 1), 9))
        elif roll < .27 and h > 110:
            antennas.append((round(x + w / 2, 1), top - 24, 1.2, 24))
        chance = .36 + block["score"] * .5
        columns = max(1, int((w - 5) // 7))
        offset = (w - (columns * 7 - 3)) / 2
        y = top + 8
        while y < HORIZON - 25:
            for column in range(columns):
                if rng.random() < chance:
                    windows[rng.randrange(6)].append((round(x + offset + column * 7, 1), round(y, 1), 4, 5))
                    count += 1
            y += 10
    colors = [p["win"][0], p["win"][1], p["win"][2], p["win"][0], p["win"][2], p["win"][1]]
    lit = "".join(
        f'<path class="w w{i}" fill="{colors[i]}" d="{rect_path(group)}"/>' for i, group in enumerate(windows)
    )
    markup = (
        f'<path fill="url(#b)" d="{rect_path(body)}"/>'
        f'<path fill="{p["rim"]}" opacity=".55" d="{rect_path(rims)}"/>'
        f'<path fill="{p["mid_a"]}" d="{rect_path(antennas)}"/>{lit}{crane(blocks[-1])}'
    )
    return markup, count


def far_city(p):
    rng = random.Random(7)
    items, x = [], 0
    while x < W:
        w, h = rng.randint(22, 58), rng.randint(70, 262)
        items.append((x, HORIZON - h, w, h))
        x += w
    return f'<path fill="{p["far"]}" opacity=".75" d="{rect_path(items)}"/>'


def tower(p, cx=1010):
    return f"""<g>
<path fill="url(#t)" d="M{cx-11} 452L{cx-4} 196H{cx+4}L{cx+11} 452Z"/>
<path fill="{p['win'][2]}" class="w w3" d="{rect_path([(cx - 1, y, 2, 4) for y in range(214, 442, 8)])}"/>
<path fill="{p['tower']}" d="M{cx-3.5} 150L{cx-1.3} 54H{cx+1.3}L{cx+3.5} 150Z"/>
<rect x="{cx-.6}" y="26" width="1.2" height="30" fill="{p['tower']}"/>
<circle cx="{cx}" cy="172" r="46" fill="url(#halo)"/>
<path fill="{p['tower']}" d="M{cx-24} 158L{cx-6} 145H{cx+6}L{cx+24} 158Z"/>
<path fill="url(#ball)" d="M{cx-31} 158H{cx+31}L{cx+24} 177L{cx+10} 198H{cx-10}L{cx-24} 177Z"/>
<rect x="{cx-28}" y="163" width="56" height="7" rx="2" fill="{p['tower_dark']}"/>
<path fill="{p['win'][2]}" class="w w2" d="{rect_path([(cx - 25 + i * 6, 165, 3, 3) for i in range(9)])}"/>
<circle class="beacon" cx="{cx}" cy="26" r="9" fill="{p['glow']}" opacity=".35"/>
<circle class="beacon" cx="{cx}" cy="26" r="2.6" fill="{p['glow']}"/>
</g>"""


def viaduct(p):
    arches = "".join(
        f"M{x} 470v-5a15 11 0 0 1 30 0v5z" for x in range(6, W, 42)
    )
    return (
        f'<rect x="0" y="447" width="{W}" height="23" fill="{p["mid_b"]}"/>'
        f'<rect x="0" y="447" width="{W}" height="1.5" fill="{p["rim"]}" opacity=".7"/>'
        f'<path fill="{p["arch"]}" d="{arches}"/>'
    )


def train(p):
    cars = []
    for i in range(4):
        x = i * 76
        panes = "".join(f'<rect x="{x + 8 + n * 11}" y="5" width="7" height="6" rx="1" fill="#fff0b8"/>' for n in range(6))
        cars.append(
            f'<rect x="{x}" width="72" height="17" rx="3" fill="#c8102e"/>'
            f'<rect x="{x}" y="12" width="72" height="5" rx="1" fill="#f4f4f4"/>{panes}'
        )
    return f'<g class="train" transform="translate(0 430)">{"".join(cars)}</g>'


def stars(p):
    rng = random.Random(52)
    still, twinkle = [], []
    for index in range(190):
        x, y, r = rng.randint(4, W - 4), rng.randint(4, 330), rng.choice([.5, .7, .9, 1.2, 1.6])
        star = f'<circle cx="{x}" cy="{y}" r="{r}"'
        if index % 5 == 0:
            twinkle.append(f'{star} class="tw" style="animation-delay:-{rng.uniform(0, 6):.1f}s"/>')
        else:
            still.append(f'{star} opacity="{rng.uniform(.25, .85):.2f}"/>')
    return f'<g fill="{p["star"]}" opacity="{p["star_op"]}">{"".join(still)}{"".join(twinkle)}</g>'


def hero(weeks, theme):
    p = PALETTES[theme]
    skyline, count = city(weeks, p)
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in zip((0, .3, .55, .74, .79), p["sky"]))
    flicker = "".join(f".w{i}{{animation:f {5 + i * 1.7:.1f}s ease-in-out -{i * 1.3:.1f}s infinite}}" for i in range(6))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="hero-title hero-desc">
<title id="hero-title">Amer Malik Mohammed, web developer in Düsseldorf</title>
<desc id="hero-desc">An animated Düsseldorf skyline with the Rheinturm at {'night' if theme == 'dark' else 'dawn'}. Each building is one week of GitHub contributions.</desc>
<defs>
<linearGradient id="s" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient>
<linearGradient id="b" x1="0" y1="200" x2="0" y2="{HORIZON}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{p['mid_a']}"/><stop offset="1" stop-color="{p['mid_b']}"/></linearGradient>
<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{p['tower']}"/><stop offset="1" stop-color="{p['tower_dark']}"/></linearGradient>
<radialGradient id="ball" cx=".36" cy=".3" r=".85"><stop offset="0" stop-color="#ffffff"/><stop offset=".42" stop-color="{p['tower']}"/><stop offset="1" stop-color="{p['tower_dark']}"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{p['win'][2]}" stop-opacity=".42"/><stop offset="1" stop-color="{p['win'][2]}" stop-opacity="0"/></radialGradient>
<radialGradient id="mg"><stop offset="0" stop-color="{p['moon']}" stop-opacity=".5"/><stop offset=".35" stop-color="{p['moon']}" stop-opacity=".12"/><stop offset="1" stop-color="{p['moon']}" stop-opacity="0"/></radialGradient>
<linearGradient id="wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['water_a']}"/><stop offset="1" stop-color="{p['water_b']}"/></linearGradient>
<linearGradient id="rf" x1="0" y1="{HORIZON}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity=".62"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="rm"><rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#rf)"/></mask>
<filter id="blur" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="ripple" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".005 .085" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="7" xChannelSelector="R" yChannelSelector="G"/></filter>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<g id="city">{far_city(p)}{skyline}{tower(p)}</g>
</defs>
<style>
.sans{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans","Noto Sans Arabic",Helvetica,Arial,sans-serif}}
.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}}
@keyframes f{{0%,100%{{opacity:1}}45%{{opacity:.92}}50%{{opacity:.3}}56%{{opacity:.95}}}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
@keyframes b{{0%,100%{{opacity:1}}50%{{opacity:.12}}}}
@keyframes a{{0%,100%{{opacity:.22}}50%{{opacity:.52}}}}
@keyframes rail{{from{{transform:translate(-340px,430px)}}to{{transform:translate(1340px,430px)}}}}
@keyframes hi{{0%{{opacity:0;transform:translateY(8px)}}4%,29%{{opacity:1;transform:none}}33%,100%{{opacity:0;transform:translateY(-8px)}}}}
@keyframes up{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:none}}}}
@keyframes shoot{{0%,91%{{opacity:0;transform:translate(0,0)}}92%{{opacity:1}}97%,100%{{opacity:0;transform:translate(-330px,150px)}}}}
@keyframes sh{{0%,100%{{transform:translateX(-7px)}}50%{{transform:translateX(7px)}}}}
{flicker}
.tw{{animation:tw 5s ease-in-out infinite}}.beacon{{animation:b 2.2s ease-in-out infinite}}
.au{{animation:a 9s ease-in-out infinite}}.train{{animation:rail 17s linear infinite}}
.hi{{opacity:0;animation:hi 10.5s linear infinite}}.up{{opacity:0;animation:up .9s cubic-bezier(.2,.8,.2,1) .15s forwards}}.up2{{animation-delay:.4s}}
.shoot{{opacity:0;animation:shoot 13s linear infinite}}.sheen{{animation:sh 6s ease-in-out infinite}}
@keyframes hk{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(16px)}}}}.hook{{animation:hk 5s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{.w,.tw,.beacon,.au,.train,.shoot,.sheen,.hook{{animation:none}}.train{{transform:translate(620px,430px)}}.up{{animation:none;opacity:1}}.hi{{animation:none}}.hi0{{opacity:1}}}}
</style>
<g clip-path="url(#frame)">
<rect width="{W}" height="{HORIZON}" fill="url(#s)"/>
{stars(p)}
<g filter="url(#blur)">
<path class="au" fill="{p['aurora'][0]}" d="M-60 170C180 60 390 250 640 130S1040 40 1340 170V235C1040 120 860 260 620 205S190 150 -60 250Z"/>
<path class="au" style="animation-delay:-3s" fill="{p['aurora'][1]}" d="M-60 90C240 10 450 140 720 70S1100 10 1340 90V150C1090 80 900 170 680 130S210 80 -60 160Z"/>
<path class="au" style="animation-delay:-6s" fill="{p['aurora'][2]}" d="M200 280C430 180 640 330 880 230S1180 190 1340 260V320C1120 260 940 360 700 310S400 270 200 340Z"/>
</g>
<circle cx="1168" cy="104" r="130" fill="url(#mg)"/><circle cx="1168" cy="104" r="34" fill="{p['moon']}"/>
<path class="shoot" stroke="#fff" stroke-width="1.6" stroke-linecap="round" d="M1050 40l46 -21"/>
<use href="#city" xlink:href="#city"/>
{train(p)}
{viaduct(p)}
<rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#wg)"/>
<g mask="url(#rm)"><g filter="url(#ripple)"><use href="#city" xlink:href="#city" transform="matrix(1 0 0 -.62 0 {HORIZON * 1.62:.1f})"/></g></g>
<g class="sheen" fill="#fff" opacity=".2"><rect x="150" y="492" width="130" height="1.3"/><rect x="520" y="511" width="210" height="1.3"/><rect x="930" y="499" width="170" height="1.3"/><rect x="310" y="538" width="150" height="1.3"/><rect x="820" y="552" width="240" height="1.3"/></g>
<g class="sans" fill="{p['fg']}">
<g font-size="34" font-weight="500" fill="{p['muted']}">
<text class="hi hi0" x="64" y="96">Hallo,</text>
<text class="hi" style="animation-delay:3.5s" x="64" y="96">Hello,</text>
<text class="hi" style="animation-delay:7s" x="858" y="96" direction="rtl" xml:lang="ar">مرحبا،</text>
</g>
<text class="up" x="62" y="168" font-size="74" font-weight="800" letter-spacing="-1.5">Amer Malik Mohammed</text>
<text class="up up2" x="64" y="212" font-size="26" fill="{p['muted']}">Web developer in Düsseldorf. Mostly Shopware and Symfony.</text>
</g>
<g class="mono" font-size="14" fill="{p['fg']}" opacity=".78">
<text x="32" y="580">51.2277° N, 6.7735° E</text>
<text x="{W - 32}" y="580" text-anchor="end">this skyline is my last 12 months on GitHub. taller = busier week.</text>
</g>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21" fill="none" stroke="#ffffff" stroke-opacity=".14" stroke-width="2"/>
</svg>
"""
    return svg, count


def certificate(windows, theme):
    dark = theme == "dark"
    bg, ink, soft, gold, stamp = (
        ("#11131f", "#f5efe0", "#a8a39a", "#d9b566", "#ff5c6c") if dark else ("#fdf8ec", "#2a2433", "#756d66", "#a77f26", "#cf2338")
    )
    rows = [
        ("Lines of this profile written by Claude", "0*"),
        ("Times it said “You're absolutely right!”", "0"),
        ("Skyline windows placed by hand, one at a time", f"{windows:,}"),
        ("Hours of sleep lost doing all of this manually", "all of them"),
    ]
    row_markup = ""
    for index, (label, value) in enumerate(rows):
        y = 196 + index * 46
        row_markup += (
            f'<g class="row" style="animation-delay:{.25 + index * .22:.2f}s">'
            f'<text x="130" y="{y}" fill="{ink}">{label}</text>'
            f'<line x1="130" x2="1150" y1="{y + 11}" y2="{y + 11}" stroke="{soft}" stroke-dasharray="2 6"/>'
            f'<text x="1150" y="{y}" text-anchor="end" fill="{gold}" font-weight="700">{value}</text></g>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 540" width="1280" height="540" role="img" aria-labelledby="ct">
<title id="ct">A joke certificate claiming this profile was made entirely by hand and that Claude definitely did not help.</title>
<style>
.serif{{font-family:Georgia,"Times New Roman","Liberation Serif",serif}}.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
@keyframes r{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes sign{{to{{stroke-dashoffset:0}}}}
@keyframes slam{{0%{{opacity:0;transform:translate(1040px,425px) rotate(-14deg) scale(3.2)}}70%{{opacity:1;transform:translate(1040px,425px) rotate(-14deg) scale(.93)}}100%{{opacity:.92;transform:translate(1040px,425px) rotate(-14deg) scale(1)}}}}
.row{{opacity:0;animation:r .5s ease-out forwards}}.sig{{stroke-dasharray:900;stroke-dashoffset:900;animation:sign 1.5s ease-in-out 1.3s forwards}}
.stamp{{opacity:0;transform:translate(1040px,425px) rotate(-14deg);animation:slam .36s cubic-bezier(.3,0,.8,.3) 2.8s forwards}}
@media (prefers-reduced-motion:reduce){{.row,.sig,.stamp{{animation:none;opacity:1;stroke-dashoffset:0}}.stamp{{opacity:.92}}}}
</style>
<rect x="1" y="1" width="1278" height="538" rx="20" fill="{bg}" stroke="{gold}" stroke-width="2"/>
<rect x="16" y="16" width="1248" height="508" rx="12" fill="none" stroke="{gold}" stroke-opacity=".5"/>
<g class="serif">
<text x="640" y="72" text-anchor="middle" font-size="16" letter-spacing="6" fill="{gold}">OFFICIAL AND LEGALLY MEANINGLESS</text>
<text x="640" y="124" text-anchor="middle" font-size="44" font-weight="700" fill="{ink}">Certificate of Human Authorship</text>
<g font-size="23">{row_markup}</g>
<path class="sig" fill="none" stroke="{ink}" stroke-width="2.6" stroke-linecap="round" d="M136 432c18-44 32-60 38-50s-20 62-14 62 26-40 36-38-6 30 4 30 18-24 28-22-4 22 8 20 20-22 32-18 0 18 14 14 34-20 60-16 44 8 96-8"/>
<line x1="130" x2="520" y1="456" y2="456" stroke="{soft}"/>
<text x="130" y="480" font-size="16" fill="{soft}">Amer, a definitely organic human</text>
<text x="130" y="507" font-size="15" font-style="italic" fill="{soft}">* Claude was in the room strictly for emotional support.</text>
</g>
<g class="stamp" fill="none" stroke="{stamp}">
<circle r="82" stroke-width="5"/><circle r="70" stroke-width="1.5"/>
<g class="mono" fill="{stamp}" stroke="none" text-anchor="middle" font-weight="800">
<text y="-12" font-size="34">100%</text><text y="22" font-size="27">HUMAN</text><text y="46" font-size="12">(trust me)</text>
</g>
</g>
</svg>
"""


def pill(label, theme):
    dark = theme == "dark"
    bg, edge, fg, dot = ("#161b2e", "#3a3f63", "#f0f6fc", "#39d353") if dark else ("#ffffff", "#d1d9e0", "#1f2328", "#1a7f37")
    arabic = bool(re.search(r"[؀-ۿ]", label))
    width = 52 + round(len(label) * (6.6 if arabic else 8.8))
    safe = label.replace("&", "&amp;")
    dot_x = width - 20 if arabic else 20
    text_x = width - 34 if arabic else 34
    direction = ' direction="rtl" xml:lang="ar"' if arabic else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="38" viewBox="0 0 {width} 38" role="img" aria-label="{safe}">
<rect x=".75" y=".75" width="{width - 1.5}" height="36.5" rx="18.25" fill="{bg}" stroke="{edge}" stroke-width="1.5"/>
<circle cx="{dot_x}" cy="19" r="4" fill="{dot}"/>
<text x="{text_x}" y="24"{direction} font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans','Noto Sans Arabic',Helvetica,Arial,sans-serif" font-size="15" font-weight="600" fill="{fg}">{safe}</text>
</svg>
"""


PILLS = {
    "website": "Website", "blog-en": "Blog", "blog-de": "Blog (DE)", "blog-ar": "المدونة",
    "youtube": "YouTube", "linkedin": "LinkedIn", "x": "X",
}


def main(argv):
    assets = pathlib.Path(argv[1] if len(argv) > 1 else "assets")
    try:
        weeks = fetch_weeks()
    except CalendarError as error:
        print(f"::warning::Skyline not updated: {error}")
        return 0
    assets.mkdir(parents=True, exist_ok=True)
    windows = 0
    for theme in PALETTES:
        svg, windows = hero(weeks, theme)
        (assets / f"hero-{theme}.svg").write_text(svg, encoding="utf-8")
        (assets / f"certificate-{theme}.svg").write_text(certificate(windows, theme), encoding="utf-8")
        for slug, label in PILLS.items():
            (assets / f"nav-{slug}-{theme}.svg").write_text(pill(label, theme), encoding="utf-8")
    print(f"Skyline drawn: {len(weeks)} weeks, {windows} windows.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

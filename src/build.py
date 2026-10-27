import os
import re, urllib.parse, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pix import SPRITE

W = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = os.path.abspath(W + '..') + '/'

# ---------- construction spot: your own GIF at images/construction.gif ----------
CONSTRUCTION = """<div class="construction">
        <!-- Put your GIF at images/construction.gif -->
        <img class="fb" data-srcs="images/construction.gif|construction.gif" data-missing="construction.gif goes here (images/construction.gif)" alt="Under construction">
      </div>"""
import profiles
ORB = open(W + 'orb96.b64').read().strip()

# ---------- "Tubzcave" Frutiger-Aero WordArt (static SVG, no animation) ----------
def make_wordart():
    return ('<span class="wm" role="img" aria-label="Tubzcave"><span class="wm-orb" aria-hidden="true"></span>'
            '<span class="wm-txt" aria-hidden="true"><span class="wm-t">Tubzcave</span><span class="wm-t wm-r">Tubzcave</span></span></span>')
WORDART = make_wordart()

# ---------- Vista-aurora style background (dim, with glass streaks) ----------
bg_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="base" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000000"/><stop offset=".38" stop-color="#050f18"/><stop offset=".72" stop-color="#0d2c46"/><stop offset="1" stop-color="#2f74b0"/></linearGradient>
<radialGradient id="glow" cx=".5" cy="1.05" r=".75"><stop offset="0" stop-color="#4fa3ec" stop-opacity=".6"/><stop offset="1" stop-color="#4fa3ec" stop-opacity="0"/></radialGradient>
<radialGradient id="glow2" cx=".12" cy=".18" r=".45"><stop offset="0" stop-color="#1c4a73" stop-opacity=".45"/><stop offset="1" stop-color="#1c4a73" stop-opacity="0"/></radialGradient>
<linearGradient id="sw1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfe6ff" stop-opacity="0"/><stop offset=".45" stop-color="#eaf4ff" stop-opacity=".75"/><stop offset=".75" stop-color="#8fc2f5" stop-opacity=".4"/><stop offset="1" stop-color="#8fc2f5" stop-opacity="0"/></linearGradient>
<linearGradient id="sw2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9fcdf7" stop-opacity="0"/><stop offset=".5" stop-color="#bfe0ff" stop-opacity=".5"/><stop offset="1" stop-color="#6fb0ee" stop-opacity="0"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="b1" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="b2" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.5"/></filter>
</defs>
<rect width="1600" height="900" fill="url(#base)"/>
<rect width="1600" height="900" fill="url(#glow2)"/><rect width="1600" height="900" fill="url(#glow)"/>
<g filter="url(#b1)" opacity=".7">
<path d="M-100 60C450 190 1000 470 1700 730C1000 540 450 280 -100 130Z" fill="url(#sw2)"/>
<path d="M1700 20C1250 190 800 430 300 920C860 560 1280 330 1700 120Z" fill="url(#sw2)" opacity=".6"/>
</g>
<g filter="url(#b2)">
<path d="M-100 80C450 200 1000 480 1700 722C1000 520 450 262 -100 112Z" fill="url(#sw1)"/>
<path d="M-100 150C400 260 900 520 1700 800C940 590 420 330 -100 176Z" fill="url(#sw2)" opacity=".8"/>
<path d="M1700 60C1260 210 820 440 340 900C880 570 1290 350 1700 140Z" fill="url(#sw2)" opacity=".75"/>
</g>
<g fill="url(#gl)">
<polygon points="860,0 1040,0 640,900 460,900"/>
<polygon points="1200,0 1290,0 880,900 790,900" opacity=".7"/>
<polygon points="420,0 480,0 90,900 30,900" opacity=".6"/>
</g>
</svg>'''
BG = 'data:image/svg+xml,' + urllib.parse.quote(bg_svg.replace('\n', ''), safe="/:=,;()' ")

# ---------- frozen-in-2001 stock ticker (approximate Dec 31, 2001 closes) ----------
ITEMS = [
    ('DJIA', '10,021.50', '-', 41.78), ('NASDAQ', '1,950.40', '-', 5.78), ('S&amp;P 500', '1,148.08', '-', 6.17),
    ('MSFT', '66.25', '+', 0.34), ('INTC', '31.45', '-', 0.22), ('CSCO', '18.11', '+', 0.11),
    ('AAPL', '21.51', '-', 0.12), ('AMZN', '10.82', '+', 0.24), ('YHOO', '17.74', '-', 0.30),
    ('AOL', '32.10', '+', 0.15), ('IBM', '120.96', '-', 0.78), ('DELL', '27.18', '+', 0.06),
    ('SUNW', '12.50', '-', 0.09), ('ORCL', '13.81', '+', 0.05), ('LU', '6.30', '-', 0.04),
    ('NOK', '24.53', '+', 0.20), ('QCOM', '50.50', '-', 0.44), ('JDSU', '8.74', '+', 0.07),
    ('EBAY', '66.90', '+', 0.52), ('WCOM', '14.08', '-', 0.10), ('ENE', '0.60', '-', 0.03),
    ('GE', '40.08', '+', 0.14), ('KO', '47.15', '-', 0.19), ('DIS', '20.72', '+', 0.08),
    ('MCD', '26.47', '-', 0.11), ('XOM', '39.30', '+', 0.17), ('WMT', '57.55', '-', 0.26),
]
def group():
    parts = ['<span class="tk tk-flat"><span class="tk-s">MARKET FROZEN 12/31/2001 4:00PM ET</span></span>']
    for sym, px, sign, ch in ITEMS:
        cls = 'tk-up' if sign == '+' else 'tk-dn'
        arrow = '&#9650;' if sign == '+' else '&#9660;'
        parts.append(f'<span class="tk"><span class="tk-s">{sym}</span><span class="tk-p">{px}</span><span class="{cls}">{arrow}{ch:.2f}</span></span>')
    return ''.join(parts)
TICKER = ('<div class="ticker" data-anim role="marquee" aria-label="Stock prices frozen in 2001"><div class="ticker-track">'
          '<div class="tk-group">' + group() + '</div><div class="tk-group" aria-hidden="true">' + group() + '</div></div></div>')

# ---------- shared pieces ----------
MUSIC_BTN = '''<button id="musicBtn" type="button" aria-label="Play music">
  <svg class="icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg>
  <svg class="icon-pause" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
</button>'''

def orb(gid, glyph):
    return (f'<svg viewBox="0 0 40 40" aria-hidden="true"><defs><radialGradient id="{gid}" cx=".35" cy=".25" r=".9">'
            f'<stop offset="0" stop-color="#9fe0ff"/><stop offset="1" stop-color="#0a56bd"/></radialGradient></defs>'
            f'<circle cx="20" cy="20" r="18" fill="url(#{gid})" stroke="#06306b"/>{glyph}'
            f'<path d="M5 17A15 15 0 0 1 35 17Q20 24 5 17Z" fill="#fff" opacity=".45"/></svg>')

HOME = orb('gOrbHome', '<path d="M20 9.5L9.5 19.5H13V29.5H18V23H22V29.5H27V19.5H30.5Z" fill="#fff"/>')
ABOUT = orb('gOrbAbout', '<circle cx="20" cy="12.5" r="2.4" fill="#fff"/><rect x="17.8" y="17" width="4.4" height="13" rx="1.8" fill="#fff"/>')
# exact pixel-art cat icon, converted from the uploaded 1.png (18x18)
from PIL import Image as _Img
def _cat_icon():
    im = _Img.open('/mnt/user-data/uploads/1.png').convert('RGBA')
    w, h = im.size
    px = im.load()
    rects = []
    for y in range(h):
        x = 0
        while x < w:
            c = px[x, y]
            if c[3] == 0:
                x += 1
                continue
            x2 = x
            while x2 + 1 < w and px[x2 + 1, y] == c:
                x2 += 1
            rects.append('<rect x="%d" y="%d" width="%d" height="1" fill="#%02x%02x%02x"/>' % (x, y, x2 - x + 1, c[0], c[1], c[2]))
            x = x2 + 1
    return ('<svg viewBox="0 0 %d %d" shape-rendering="crispEdges" aria-hidden="true"><defs><clipPath id="cMimi"><rect width="%d" height="%d" rx="4"/></clipPath></defs>'
            '<g clip-path="url(#cMimi)">%s</g>'
            '<path d="M0 0H%d V8Q%d 11 0 8Z" fill="#fff" opacity=".28" shape-rendering="geometricPrecision" clip-path="url(#cMimi)"/></svg>') % (w, h, w, h, ''.join(rects), w, w // 2)
MIMI = _cat_icon()

def taskbar(current):
    def a(href, label, svg, key):
        cur = ' aria-current="page"' if key == current else ''
        return (f'  <a class="tb-link" href="{href}"{cur}>\n    {svg}\n    <span class="tb-label">{label}</span>\n  </a>\n')
    return ('<!-- ============ TASKBAR (copy into every page; add one link per new page) ============ -->\n'
            '<nav id="taskbar" aria-label="Main navigation">\n'
            + a('index.html', 'Home', HOME, 'home') + a('about.html', 'About', ABOUT, 'about') + a('mimi.html', 'Mimi', MIMI, 'mimi')
            + '</nav>')

# ---------- big wide rat ----------
RAT = '''<!-- Put your picture at images/rat.png (or images/rat.jpg) -->
  <img class="fb rat" data-srcs="images/rat.png|images/rat.jpg|images/rat.jpeg|rat.png|rat.jpg" data-missing="Put rat.png (or rat.jpg) in the images folder" alt="Rat">'''

MOBILE_JS = '''<script>(function(){var d=document.documentElement,q=window.matchMedia("(max-width:700px),(hover:none) and (pointer:coarse) and (max-width:960px)");function f(){d.classList.toggle("m",q.matches)}f();if(q.addEventListener)q.addEventListener("change",f);else q.addListener(f)})();</script>'''

def page(title, body_main, current, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{MOBILE_JS}
<link rel="stylesheet" href="style.css">
</head>
<body>

{MUSIC_BTN}

{taskbar(current)}

{body_main}

<script src="site.js"></script>
</body>
</html>
'''

ABOUT_HTML = page("About - Tubzcave", '<main class="solo">\n  ' + RAT + '\n</main>', 'about')
MIMI_HTML = page("Mimi - Tubzcave",
    '<main class="solo">\n  <!-- Put your picture at images/Mimi.png (also tries Mimi.png, images/mimi.png, mimi.png) -->\n'
    '  <img class="fb mimi" data-srcs="images/Mimi.png|Mimi.png|images/mimi.png|mimi.png" data-missing="Mimi.png goes here" alt="Mimi">\n</main>', 'mimi')

tpl = open(W + 'index.tpl.html', encoding='utf-8').read()
for k, v in {'{{SPRITE}}': SPRITE, '{{MUSIC_BTN}}': MUSIC_BTN, '{{TASKBAR}}': taskbar('home'),
             '{{TICKER}}': TICKER, '{{CONSTRUCTION}}': CONSTRUCTION, '{{ORB}}': ORB, '{{WORDART}}': WORDART, '{{PROFILES_L}}': profiles.LEFT, '{{PROFILES_R}}': profiles.RIGHT}.items():
    assert k in tpl, k
    tpl = tpl.replace(k, v)
css = (open(W + 'style.tpl.css', encoding='utf-8').read() + open(W + 'profiles.css', encoding='utf-8').read() + (open(W + 'mobile.css', encoding='utf-8').read() if os.path.exists(W + 'mobile.css') else '')).replace('{{BG}}', BG)

open(OUT + 'index.html', 'w', encoding='utf-8').write(tpl)
open(OUT + 'about.html', 'w', encoding='utf-8').write(ABOUT_HTML)
open(OUT + 'mimi.html', 'w', encoding='utf-8').write(MIMI_HTML)
open(OUT + 'style.css', 'w', encoding='utf-8').write(css)
open(OUT + 'site.js', 'w', encoding='utf-8').write(open(W + 'site.js', encoding='utf-8').read())
print('built', len(tpl), len(css))

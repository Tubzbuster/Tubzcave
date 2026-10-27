import math

def emit(sym_id, N, g):
    out = [f'<symbol id="{sym_id}" viewBox="0 0 {N} {N}" shape-rendering="crispEdges">']
    for y in range(N):
        x = 0
        while x < N:
            c = g.get((x, y))
            if c is None:
                x += 1
                continue
            x2 = x
            while g.get((x2 + 1, y)) == c:
                x2 += 1
            out.append(f'<rect x="{x}" y="{y}" width="{x2 - x + 1}" height="1" fill="{c}"/>')
            x = x2 + 1
    out.append('</symbol>')
    return ''.join(out)

def dseg(px, py, a, b):
    ax, ay = a; bx, by = b
    vx, vy = bx - ax, by - ay
    L = vx * vx + vy * vy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * vx + (py - ay) * vy) / L))
    return math.hypot(px - (ax + t * vx), py - (ay + t * vy))

def outline_from(fill, N):
    o = set()
    for (x, y) in fill:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p not in fill and 0 <= p[0] < N and 0 <= p[1] < N:
                    o.add(p)
    return o

# ---------- CD-ROM disc ----------
def cd():
    N = 24; g = {}
    R = 10.6
    for y in range(N):
        for x in range(N):
            dx, dy = x + .5 - 12, y + .5 - 12
            d = math.hypot(dx, dy)
            if d > R:
                continue
            if d > R - 1.1:
                c = '#34475c'
            elif d < 2.3:
                continue
            elif d < 3.3:
                c = '#34475c'
            elif d < 5.2:
                c = '#eef3f9'
            else:
                ang = math.degrees(math.atan2(dy, dx)) % 360
                if 15 < ang < 75: c = '#86d8ee'
                elif 75 <= ang < 110: c = '#c8a2f2'
                elif 195 < ang < 255: c = '#86d8ee'
                elif 255 <= ang < 290: c = '#f0c0e8'
                else:
                    t = (-dx - dy) / (2 * R)
                    c = '#ffffff' if t > .38 else ('#8fa3ba' if t < -.38 else '#cfd9e6')
            g[(x, y)] = c
    return g

# ---------- upside-down, inverted "not-steam" badge ----------
def warez():
    N = 24; g = {}
    dark, light = '#1b2838', '#e6edf5'
    R = 11
    for y in range(N):
        for x in range(N):
            px, py = x + .5, y + .5
            d = math.hypot(px - 12, py - 12)
            if d > R:
                continue
            if d > R - 1.2:
                c = dark
            else:
                c = light
                if (px - 12) + (py - 12) < -9:
                    c = '#ffffff'
                # glyph (flipped vertically: big ring lower right, small circle upper left)
                if math.hypot(px - 14.5, py - 14.5) <= 5.0:
                    c = dark
                    if math.hypot(px - 14.5, py - 14.5) <= 2.3:
                        c = light
                    if math.hypot(px - 14.5, py - 14.5) <= 0.9:
                        c = dark
                if math.hypot(px - 8.5, py - 8.5) <= 2.6:
                    c = dark
                if dseg(px, py, (8.5, 8.5), (12.5, 12.5)) <= 1.2:
                    c = dark
            g[(x, y)] = c
    return g

# ---------- yellow runner ----------
def aim():
    N = 24
    segs = [((13, 8.5), (10.5, 14)), ((13, 9), (17.5, 11)), ((17.5, 11), (20, 8)),
            ((12.5, 9.5), (8, 10)), ((8, 10), (5, 12.5)), ((10.5, 14), (15, 16.5)),
            ((15, 16.5), (14, 21.5)), ((10.5, 14), (7, 18)), ((7, 18), (3.5, 17))]
    fill = set()
    for y in range(N):
        for x in range(N):
            px, py = x + .5, y + .5
            if any(dseg(px, py, a, b) <= 1.35 for a, b in segs) or math.hypot(px - 14.5, py - 4.7) <= 3.3:
                fill.add((x, y))
    g = {}
    for p in outline_from(fill, N):
        g[p] = '#5c4300'
    for p in fill:
        g[p] = '#ffd21f'
        if p[0] + p[1] > 24 and p[1] > 10:
            g[p] = '#e8ad00'
    for (x, y) in fill:
        if math.hypot(x + .5 - 13.4, y + .5 - 3.6) < 1.5:
            g[(x, y)] = '#fff6a8'
    return g

# ---------- recycle bin ----------
def binicon():
    N = 24; g = {}
    ol, body, rib, lid, green = '#46586b', '#dde5ee', '#b6c3d1', '#c8d3df', '#2fa84f'
    for y in range(9, 22):
        t = (y - 9) / 12
        xl = int(round(6 + 1.5 * t)); xr = int(round(17 - 1.5 * t))
        for x in range(xl, xr + 1):
            c = body
            if x in (xl, xr) or y == 21:
                c = ol
            elif xl + 2 <= x <= xr - 2 and (x - xl) % 3 == 2 and 11 <= y <= 19:
                c = rib
            g[(x, y)] = c
    for x in range(4, 20):
        g[(x, 7)] = ol
    for x in range(4, 20):
        g[(x, 8)] = ol if x in (4, 19) else lid
    for x in range(10, 14):
        g[(x, 5)] = ol
    for x in (9, 14):
        g[(x, 6)] = ol
    for x in range(10, 14):
        g[(x, 6)] = lid
    for p in [(9, 12), (10, 12), (11, 12), (12, 12), (13, 12), (14, 12), (10, 13), (11, 13), (12, 13),
              (13, 13), (11, 14), (12, 14)]:
        g[p] = green
    return g

# ---------- key ----------
def key():
    N = 24
    fill = set()
    segs = [((10.5, 11.5), (19, 20)), ((15.5, 16), (18, 13.5)), ((18, 18.5), (20.5, 16))]
    for y in range(N):
        for x in range(N):
            px, py = x + .5, y + .5
            d = math.hypot(px - 7, py - 8)
            if (1.9 <= d <= 4.4) or any(dseg(px, py, a, b) <= (1.2 if i == 0 else .9) for i, (a, b) in enumerate(segs)):
                fill.add((x, y))
    g = {}
    for p in outline_from(fill, N):
        g[p] = '#6b4e00'
    for p in fill:
        g[p] = '#f2c230'
        if p[0] + p[1] < 14:
            g[p] = '#ffe27a'
    return g

# ---------- film strip (fallback thumbnail) ----------
def film():
    N = 24; g = {}
    for y in range(4, 20):
        for x in range(2, 22):
            g[(x, y)] = '#0b1730' if (y in (4, 19) or x in (2, 21)) else '#2a3f5f'
    for x in range(3, 21, 3):
        for y in (5, 17):
            g[(x, y)] = '#ffffff'; g[(x + 1, y)] = '#ffffff'
            g[(x, y + 1)] = '#ffffff'; g[(x + 1, y + 1)] = '#ffffff'
    for y in range(8, 16):
        for x in range(5, 19):
            g[(x, y)] = '#6fc3f0' if y < 12 else '#2a85e0'
    for p in [(11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (12, 10), (12, 11), (12, 12), (13, 11)]:
        g[p] = '#ffffff'
    return g

# ---------- start flag ----------

def flag():
    # four clean panes, centered; right panes sit one pixel higher than the left (a tiny wave)
    g = {}
    def pane(x0, y0, c):
        for y in range(y0, y0 + 6):
            for x in range(x0, x0 + 6):
                g[(x, y)] = c
    pane(1, 2, '#f25022'); pane(9, 1, '#7fba00')
    pane(1, 9, '#00a4ef'); pane(9, 8, '#ffb900')
    # soft highlight on the top row of every pane
    for (x, y), c in list(g.items()):
        if (x, y - 1) not in g:
            g[(x, y)] = {'#f25022': '#ff7a52', '#7fba00': '#a9e02a', '#00a4ef': '#4cc4ff', '#ffb900': '#ffd34d'}[c]
    return g

def _grid(N=16):
    return {}

def _rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[(x, y)] = c

def ico_folder():
    g = {}
    ol, hi, mid = '#8a6200', '#ffe27a', '#f2bd2e'
    _rect(g, 2, 3, 7, 4, ol); _rect(g, 1, 4, 14, 13, ol)
    _rect(g, 2, 4, 6, 5, hi); _rect(g, 2, 6, 13, 12, mid); _rect(g, 2, 6, 13, 7, hi)
    return g

def ico_pic():
    g = {}
    _rect(g, 1, 2, 14, 13, '#34475c'); _rect(g, 2, 3, 13, 12, '#8fd0ff')
    for x in range(2, 14):
        top = 9 - int(2 * math.sin((x - 2) / 3.2))
        for y in range(top, 13): g[(x, y)] = '#4caf50'
    _rect(g, 10, 4, 11, 5, '#ffe14a')
    return g

def ico_music():
    g = {}
    _rect(g, 6, 3, 7, 11, '#1b2838'); _rect(g, 7, 2, 12, 3, '#1b2838'); _rect(g, 11, 3, 12, 9, '#1b2838')
    _rect(g, 3, 10, 6, 12, '#1b2838'); _rect(g, 8, 8, 11, 10, '#1b2838')
    _rect(g, 4, 10, 5, 11, '#8fd0ff'); _rect(g, 9, 8, 10, 9, '#8fd0ff')
    return g

def ico_pc():
    g = {}
    _rect(g, 1, 2, 14, 11, '#34475c'); _rect(g, 2, 3, 13, 10, '#5db4ff'); _rect(g, 2, 3, 13, 5, '#bfe6ff')
    _rect(g, 6, 12, 9, 12, '#34475c'); _rect(g, 3, 13, 12, 13, '#8ea1b5')
    return g

def ico_gear():
    g = {}
    for y in range(16):
        for x in range(16):
            dx, dy = x + .5 - 8, y + .5 - 8
            d = math.hypot(dx, dy); a = math.atan2(dy, dx)
            r = 5.0 + (1.6 if math.cos(a * 4) > .35 else 0)
            if d <= r and d >= 2.2:
                g[(x, y)] = '#9fb3c8' if (dx + dy) < 0 else '#6c819a'
    return g

def ico_help():
    g = {}
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + .5 - 8, y + .5 - 8)
            if d <= 7: g[(x, y)] = '#1f6fd0' if d > 6 else '#4aa3ff'
    for p in [(6,5),(7,4),(8,4),(9,5),(9,6),(8,7),(7,8),(7,9),(7,11)]:
        g[p] = '#ffffff'; g[(p[0] + 1 if p[1] != 11 else p[0], p[1])] = '#ffffff'
    return g

def ico_power():
    g = {}
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + .5 - 8, y + .5 - 8)
            if d <= 7: g[(x, y)] = '#b02a1e' if d > 6 else '#e8584a'
    for y in range(3, 9): g[(7, y)] = '#ffffff'; g[(8, y)] = '#ffffff'
    for a in range(30, 331, 12):
        x = int(8 + 4.3 * math.cos(math.radians(a - 90))); y = int(8 + 4.3 * math.sin(math.radians(a - 90)))
        if y >= 5 or abs(x - 8) > 1: g[(x, y)] = '#ffffff'
    return g

def cat_avatar():
    from PIL import Image
    im = Image.open('/mnt/user-data/uploads/1.png').convert('RGBA')
    g = {}
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, gg, b, a = im.getpixel((x, y))
            if a: g[(x, y)] = '#%02x%02x%02x' % (r, gg, b)
    return im.size[0], g

def ico_fox():
    # left half of a fox face (8 cols); mirrored to make 16x16
    rows = [
        "........",
        ".oo.....",
        ".oDo....",
        ".oDDo...",
        ".oDOOo..",
        ".oOOOOoo",
        ".oOOOOOO",
        "oOOOOOOO",
        "oOkkOOOO",
        "oOOOOOOO",
        "oOwOOwww",
        ".oOwwwww",
        "..owwwww",
        "...owwwk",
        "....oowk",
        "......oo",
    ]
    pal = {'o': '#5a2300', 'O': '#ff8a1f', 'D': '#3a1a00', 'w': '#fff6e6', 'k': '#1b1b1b'}
    g = {}
    for y, row in enumerate(rows):
        assert len(row) == 8, row
        for x, ch in enumerate(row):
            if ch in pal:
                g[(x, y)] = pal[ch]; g[(15 - x, y)] = pal[ch]
    # a little glossy highlight on the forehead
    for p_ in [(5, 5), (6, 5)]:
        g[p_] = '#ffc27a'; g[(15 - p_[0], p_[1])] = '#ffc27a'
    return g

def ico_volume():
    g = {}
    body, dark, wave = '#d8dde6', '#4a5568', '#2a3f66'
    _rect(g, 2, 6, 4, 9, dark); _rect(g, 3, 7, 4, 8, body)       # speaker box
    for i, (x, y0, y1) in enumerate([(5, 5, 10), (6, 4, 11), (7, 3, 12)]):
        for y in range(y0, y1 + 1): g[(x, y)] = body if i < 2 else body
    for y in range(3, 13): g[(8, y)] = dark                        # cone edge
    for y in range(5, 11): g[(10, y)] = wave
    for y in range(3, 13): g[(12, y)] = wave
    g[(11, 4)] = wave; g[(11, 11)] = wave; g[(11, 6)] = None; g[(11, 9)] = None
    for k in [k for k, v in g.items() if v is None]: del g[k]
    return g


# ---------- desktop icons for the three MMO profile popups ----------
def _ell(g, cx, cy, rx, ry, c):
    for y in range(24):
        for x in range(24):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                g[(x, y)] = c

def wow_icon():
    g = {}
    # shield: gold rim, blue / navy quarters
    for y in range(2, 23):
        t = (y - 2) / 20.0
        hw = 9.2 * (1 - max(0, t - .45) / .55) ** .75 if t > .45 else 9.2
        for x in range(24):
            dx = abs(x + .5 - 12)
            if dx <= hw:
                rim = dx > hw - 1.3 or y < 3.5 or (t > .45 and dx > hw - 1.9)
                if rim: c = '#e8b83a' if (x + y) % 5 else '#fff0a0'
                else: c = '#2c6fd6' if ((x + .5 < 12) == (y < 11)) else '#14316e'
                g[(x, y)] = c
    # sword: silver blade, gold guard + grip
    for y in range(24):
        for x in range(24):
            px, py = x + .5, y + .5
            if dseg(px, py, (17.5, 4.5), (9.5, 14.5)) <= .95: g[(x, y)] = '#f2f6fb'
            if dseg(px, py, (17.5, 4.5), (18.5, 3.5)) <= 1.0: g[(x, y)] = '#ffffff'
            if dseg(px, py, (7.2, 12.4), (12.6, 16.2)) <= .95: g[(x, y)] = '#ffd34a'
            if dseg(px, py, (9.5, 14.5), (6.5, 19.5)) <= .95: g[(x, y)] = '#7a3b12'
    for (x, y) in outline_from(set(g), 24):
        g[(x, y)] = '#0a0f1c'
    return g

def df_icon():
    g = {}
    # horns
    for y in range(24):
        for x in range(24):
            px, py = x + .5, y + .5
            if dseg(px, py, (6.5, 9), (3.2, 2.2)) <= 1.5 or dseg(px, py, (17.5, 9), (20.8, 2.2)) <= 1.5:
                g[(x, y)] = '#f1e4c0'
    _ell(g, 12, 13.5, 8.6, 8.2, '#c72b12')
    _ell(g, 12, 17.2, 5.4, 4.6, '#e8683a')           # snout
    _ell(g, 12, 9.0, 8.0, 3.4, '#d83c1a')            # brow
    for sx in (7.2, 16.8):                            # eyes: yellow with slit
        _ell(g, sx, 10.6, 2.3, 1.6, '#ffe03a')
        for y in range(8, 14):
            g[(int(sx - .5 + .5), y)] = g.get((int(sx), y), '#ffe03a') if False else g.get((int(sx), y))
        g[(int(sx), 10)] = '#1a0402'; g[(int(sx), 11)] = '#1a0402'
    g[(10, 17)] = '#3a0a04'; g[(13, 17)] = '#3a0a04'  # nostrils
    for x in (8, 15):                                  # fangs
        g[(x, 20)] = '#ffffff'; g[(x, 21)] = '#ffffff'
    for (x, y) in outline_from(set(g), 24):
        g[(x, y)] = '#2a0602'
    return g

def np_icon():
    g = {}
    _ell(g, 12, 12, 11, 11, '#3b8ee8')
    for y in range(24):
        for x in range(24):
            if math.hypot(x + .5 - 12, y + .5 - 12) <= 11 and math.hypot(x + .5 - 12, y + .5 - 12) > 9.6: g[(x, y)] = '#ffffff'
    for ex, e1 in ((7, (5.5, 4)), (17, (18.5, 4))):   # ears
        for y in range(24):
            for x in range(24):
                if abs(x + .5 - ex) <= (9 - y) * .55 and 3 <= y <= 9: g[(x, y)] = '#ffc93a'
    _ell(g, 12, 13.5, 7.6, 6.8, '#ffd84a')            # face
    for sx in (9, 15):
        _ell(g, sx, 12.5, 1.4, 1.7, '#14243e'); g[(sx - 1, 11)] = '#ffffff'
    for x in range(9, 16):                             # smile
        y = 16 + (1 if 10 <= x <= 13 else 0)
        g[(x, y)] = '#a8430a'
    g[(12, 14)] = '#e8590c'; g[(11, 14)] = '#e8590c'; g[(11, 15)] = None; g.pop((11, 15), None)
    _ell(g, 6.5, 15.5, 1.2, .9, '#ff9a8a'); _ell(g, 17.5, 15.5, 1.2, .9, '#ff9a8a')
    return g

_cw, _cg = cat_avatar()

SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
          + emit('px-cd', 24, cd()) + emit('px-warez', 24, warez()) + emit('px-aim', 24, aim())
          + emit('px-bin', 24, binicon()) + emit('px-key', 24, key()) + emit('px-film', 24, film())
          + emit('px-flag', 16, flag())
          + emit('px-folder', 16, ico_folder()) + emit('px-pic', 16, ico_pic()) + emit('px-music', 16, ico_music())
          + emit('px-pc', 16, ico_pc()) + emit('px-gear', 16, ico_gear()) + emit('px-help', 16, ico_help())
          + emit('px-power', 16, ico_power()) + emit('px-cat', _cw, _cg)
          + emit('px-wow', 24, wow_icon()) + emit('px-df', 24, df_icon()) + emit('px-np', 24, np_icon())
          + emit('px-fox', 16, ico_fox()) + emit('px-vol', 16, ico_volume())
          + '<symbol id="anon" viewBox="0 0 40 40"><defs><linearGradient id="gAnon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d3d9df"/><stop offset="1" stop-color="#b4bcc5"/></linearGradient></defs><rect width="40" height="40" fill="url(#gAnon)"/><circle cx="20" cy="15.5" r="7" fill="#f4f6f8"/><path d="M5 40C5 29 11 24.5 20 24.5S35 29 35 40Z" fill="#f4f6f8"/></symbol>'
          + '''<symbol id="grape" viewBox="0 0 48 48">
<defs><radialGradient id="gGrape" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#e9c0ff"/><stop offset=".55" stop-color="#9a45d8"/><stop offset="1" stop-color="#5a1c96"/></radialGradient></defs>
<path d="M24 12Q24 6 28 3" stroke="#5b3a14" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<path d="M26 8Q36 1 43 8Q34 14 26 8Z" fill="#4caf3a" stroke="#2a6b1f"/>
<g fill="url(#gGrape)" stroke="#3d0f6b">
<circle cx="14" cy="19" r="7.5"/><circle cx="24" cy="19" r="7.5"/><circle cx="34" cy="19" r="7.5"/>
<circle cx="19" cy="30" r="7.5"/><circle cx="29" cy="30" r="7.5"/><circle cx="24" cy="40" r="7.5"/>
</g>
<g fill="#fff" opacity=".55">
<ellipse cx="11.5" cy="16" rx="2.3" ry="1.4"/><ellipse cx="21.5" cy="16" rx="2.3" ry="1.4"/><ellipse cx="31.5" cy="16" rx="2.3" ry="1.4"/>
<ellipse cx="16.5" cy="27" rx="2.3" ry="1.4"/><ellipse cx="26.5" cy="27" rx="2.3" ry="1.4"/><ellipse cx="21.5" cy="37" rx="2.3" ry="1.4"/>
</g>
</symbol>
</svg>''')

if __name__ == '__main__':
    open('/home/claude/work/sprite.html', 'w', encoding='utf-8').write(SPRITE)
    print(len(SPRITE))

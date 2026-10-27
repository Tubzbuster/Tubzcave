# ============================================================
#  EDIT YOUR CHARACTER DETAILS HERE, then re-run build.py.
#  Art: put a picture for each at images/dragonfable.png,
#  images/neopet.png and images/wow.png (jpg also works).
# ============================================================
DF = dict(name="YOUR NAME", cls="DragonLord", level="90", guild="Guild Name", armor="Armor of Placeholder", hp="9,999", mp="5,000")
NP = dict(name="PetName", species="Species", colour="Colour", age="1,234 days", mood="Happy", hunger="Not hungry", level="30", hp="150")
WOW = dict(name="Charactername", race="Race", cls="Mage", level="80", guild="Guild Name", realm="Realm", ilvl="999", ap="12,345",
           classcolor="#3FC7EB",
           items=[("e", "Epic Helm of Placeholder"), ("l", "Legendary Weapon of Placeholder"), ("r", "Rare Cloak of Placeholder"), ("e", "Epic Boots of Placeholder")])

def art(path, cls):
    srcs = '|'.join([f'images/{path}.png', f'images/{path}.jpg', f'images/{path}.jpeg', f'images/{path}.gif', f'{path}.png', f'{path}.jpg'])
    return f'<img class="fb {cls}" data-srcs="{srcs}" data-icon="anon" alt="">'

def e(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def df():
    d = {k: e(v) for k, v in DF.items()}
    return f'''<section class="pf pf-df" aria-label="DragonFable character">
  <div class="df-crest"><i class="df-horn l"></i><span>DragonFable</span><i class="df-horn r"></i></div>
  <div class="df-panel">
    <div class="df-art">{art('dragonfable', 'pf-art')}</div>
    <h3 class="df-name">{d['name']}</h3>
    <div class="df-sub">Level {d['level']} {d['cls']}</div>
    <dl class="df-stats">
      <div><dt>Guild</dt><dd>{d['guild']}</dd></div>
      <div><dt>Armor</dt><dd>{d['armor']}</dd></div>
    </dl>
    <div class="df-bar hp"><b style="width:100%"></b><span>HP {d['hp']}</span></div>
    <div class="df-bar mp"><b style="width:82%"></b><span>MP {d['mp']}</span></div>
  </div>
  <div class="df-embers" aria-hidden="true"></div>
</section>'''

def np_():
    d = {k: e(v) for k, v in NP.items()}
    return f'''<section class="pf pf-np" aria-label="Neopet profile">
  <i class="np-star s1"></i><i class="np-star s2"></i><i class="np-star s3"></i><i class="np-star s4"></i>
  <div class="np-tag">My Neopet!</div>
  <div class="np-card">
    <div class="np-art">{art('neopet', 'pf-art')}</div>
    <h3 class="np-name">{d['name']}</h3>
    <dl class="np-stats">
      <div><dt>Species</dt><dd>{d['species']}</dd></div>
      <div><dt>Colour</dt><dd>{d['colour']}</dd></div>
      <div><dt>Age</dt><dd>{d['age']}</dd></div>
      <div><dt>Mood</dt><dd>{d['mood']}</dd></div>
      <div><dt>Hunger</dt><dd>{d['hunger']}</dd></div>
      <div><dt>Level</dt><dd>{d['level']}</dd></div>
    </dl>
  </div>
  <div class="np-paws" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
</section>'''

def wow():
    d = {k: (e(v) if k != 'items' else v) for k, v in WOW.items()}
    items = ''.join(f'<li class="q-{q}">{e(n)}</li>' for q, n in d['items'])
    return f'''<section class="pf pf-wow" style="--cc:{d['classcolor']}" aria-label="World of Warcraft character">
  <i class="wow-orn tl"></i><i class="wow-orn tr"></i><i class="wow-orn bl"></i><i class="wow-orn br"></i>
  <div class="wow-plate">World of Warcraft</div>
  <div class="wow-body">
    <div class="wow-portrait"><div class="wow-ring">{art('wow', 'pf-art')}</div><span class="wow-lvl">{d['level']}</span></div>
    <h3 class="wow-name">{d['name']}</h3>
    <div class="wow-sub">Level {d['level']} {d['race']} {d['cls']}</div>
    <div class="wow-guild">&lt;{d['guild']}&gt;</div>
    <div class="wow-bar hp"><b></b><span>100%</span></div>
    <div class="wow-bar mana"><b></b><span>100%</span></div>
    <div class="wow-meta"><span>{d['realm']}</span><span>iLvl {d['ilvl']}</span><span>&#9733; {d['ap']}</span></div>
    <ul class="wow-items">{items}</ul>
  </div>
</section>'''

LEFT = df() + '\n' + np_()
RIGHT = wow()

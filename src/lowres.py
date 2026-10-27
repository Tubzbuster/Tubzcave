
import os, io

def render_lowres(out_dir, width=78, colors=28):
    """Screenshots each profile box and shrinks it into a tiny, low-res PNG (images/pf-*.png)."""
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except Exception as ex:
        print('lowres skipped:', ex); return
    os.makedirs(os.path.join(out_dir, 'images'), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        g = b.new_page(viewport={'width': 1800, 'height': 1000}, device_scale_factor=1)
        g.goto('file://' + os.path.join(out_dir, 'index.html')); g.wait_for_timeout(700)
        for key, sel in (('wow', '.pf-wow'), ('df', '.pf-df'), ('np', '.pf-np')):
            png = g.locator(sel).screenshot()
            im = Image.open(io.BytesIO(png)).convert('RGB')
            h = max(1, round(im.height * width / im.width))
            im = im.resize((width, h), Image.BOX).quantize(colors, method=Image.MEDIANCUT, dither=Image.NONE)
            im.save(os.path.join(out_dir, 'images', 'pf-%s.png' % key), optimize=True)
        b.close()
    print('lowres done')

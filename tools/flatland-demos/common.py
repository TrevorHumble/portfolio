from drv import *
SETUP = open(os.path.join(H, 'setup.py')).read()
def W(x, y): return (round(800 + 103.75 * x), round(508 - 103.75 * y))
def relaunch():
    if os.path.exists(os.path.join(H, 'ready')): os.remove(os.path.join(H, 'ready'))
    subprocess.run(['bash', os.path.join(H, 'start.sh')], env=ENV)
    time.sleep(2)
def reset(panel=False, stroke_open=False, fill_open=False, fresh=True):
    if fresh: relaunch()
    bx(SETUP)
    bx('ps=bpy.context.window_manager.flatland_panel; ps.stroke_open=%r; ps.fill_open=%r' % (stroke_open, fill_open))
    bx('ts=bpy.context.scene.tool_settings; ts.use_transform_data_origin=False')
    bx('show_panel(%r)' % panel); time.sleep(1.0)
    if panel:
        click(1586, 265, 0.1); time.sleep(0.4)
    bx("""c=ctx_view()
with bpy.context.temp_override(**c):
    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")""")
    jump(700, 900); time.sleep(0.8)
def flyout(i, tool_y=566):
    move(29, tool_y, 0.35); down(); time.sleep(0.6)
    move(110, 93 + 42 * i, 0.35); time.sleep(0.15); up(); time.sleep(0.3)
def color_active(fill=None, stroke=None, fill_on=None, stroke_on=None, width=None):
    code = 'ob=bpy.context.object\n'
    if fill_on is not None: code += 'ob.flatland_fill.enabled=%r\n' % fill_on
    if stroke_on is not None: code += 'ob.flatland_stroke.enabled=%r\n' % stroke_on
    if fill: code += 'ob.flatland_fill.enabled=True\nob.flatland_fill.color=%s\n' % fill
    if stroke: code += 'ob.flatland_stroke.enabled=True\nob.flatland_stroke.color=%s\n' % stroke
    if width: code += 'ob.flatland_stroke.width=%r\n' % width
    return bx(code)
def set_field(x, y, text, dur=0.45):
    move(x, y, dur); time.sleep(0.1); xd('click', '--repeat', 2, '--delay', 80, 1); time.sleep(0.25)
    key('ctrl+a', pause=0.1); typ(text, 110); time.sleep(0.2); key('Return', pause=0.5)
def shift_drag(x, y, dx, dur=1.0):
    move(x, y, 0.4); down(); time.sleep(0.1); xd('keydown', 'shift'); move(x + dx, y, dur); up(); xd('keyup', 'shift')
import random as _random
_RNG = _random.Random(11)
def jit(base, cv=0.15, rng=None):
    """A human pause: centred on `base`, varying about `cv` of it, lopsided toward the occasional
    longer one (lognormal), and seeded so a rerun records the same take (HUMAN-MOTION.md, Rhythm)."""
    r = rng or _RNG
    sigma = math.sqrt(math.log(1 + cv * cv))
    return base * math.exp(r.gauss(-sigma * sigma / 2, sigma))

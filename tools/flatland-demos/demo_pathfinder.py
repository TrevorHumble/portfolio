from common import *
reset(panel=True)
xs = [-2.85, -0.95, 0.95, 2.85]
bx('''xs=%r
for x in xs:
    a=add_shape("RECTANGLE", x-0.22, 0.2, fill=INK, width=1.1, height=1.1); a.flatland_stroke.enabled=False
    b=add_shape("ELLIPSE", x+0.22, -0.2, fill=SCARLET, width=1.1, height=1.1); b.flatland_stroke.enabled=False
bpy.ops.object.select_all(action="DESELECT")''' % xs)
time.sleep(0.5); shot('pf0')
jump(700, 900); time.sleep(0.6)
rec_start('pathfinder'); time.sleep(0.5)
# a different spot on each shape, the way a hand never lands twice in the same place
SQ = [(-0.55, 0.45), (-0.40, 0.62), (-0.60, 0.30), (-0.35, 0.55)]
CI = [(0.45, -0.55), (0.55, -0.35), (0.30, -0.62), (0.60, -0.45)]
BTN = [(1, -2), (-2, 1), (2, 2), (-1, -1)]
# rhythm (HUMAN-MOTION.md): the first pair is the slowest and each repeat gets a little quicker,
# every pause varies, the look at each result stays the longest pause
TEMPO = [1.0, 0.9, 0.82, 0.76]
for i, x in enumerate(xs):
    T = TEMPO[i]
    sq, ci = W(x + SQ[i][0], SQ[i][1]), W(x + CI[i][0], CI[i][1])
    if i == 2:
        # this pair is picked with a box drag on the empty paper around it
        move(*W(x - 0.95, 0.88), jit(0.55 * T)); time.sleep(jit(0.12))
        down(); time.sleep(0.06); move(*W(x + 0.92, -0.9), jit(0.5 * T)); time.sleep(0.05); up()
    else:
        first, second = (sq, ci) if i % 2 == 0 else (ci, sq)
        click(*first, dur=jit(0.55 * T), pause=jit(0.12))
        xd('keydown', 'shift'); click(*second, dur=jit(0.38 * T), pause=jit(0.1)); xd('keyup', 'shift')
    time.sleep(jit(0.18 * T))
    click(1334 + 21 * i + BTN[i][0], 212 + BTN[i][1], dur=jit(0.6 * T), pause=jit(0.12))
    time.sleep(jit(1.0 * T, cv=0.2))                          # look at the result
bx('bpy.ops.object.select_all(action="DESELECT")')
move(700, 900, 0.5); time.sleep(1.5)
print(rec_stop())
print(bx('print(sorted(o.name for o in bpy.data.objects if not o.name.startswith("flatland_")))'))

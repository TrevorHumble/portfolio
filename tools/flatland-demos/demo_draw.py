from common import *
reset()
rec_start('draw')
time.sleep(0.6)
flyout(0)                                   # Rectangle
move(450, 330, 0.4); drag(620, 455, 0.7)
print(color_active(fill='INK', stroke_on=False)); time.sleep(0.4)
flyout(1)                                   # Ellipse
move(690, 330, 0.4); down(); time.sleep(0.05); xd('keydown', 'shift'); move(815, 455, 0.6); up(); xd('keyup', 'shift')
print(color_active(fill='SCARLET', stroke_on=False)); time.sleep(0.4)
flyout(3)                                   # Star
move(880, 330, 0.4); drag(1010, 455, 0.7)
print(color_active(fill='PAPER', stroke='SCARLET', width=0.04)); time.sleep(0.4)
flyout(2)                                   # Polygon
move(1060, 330, 0.4); drag(1170, 455, 0.7)
print(color_active(fill='INK', stroke_on=False)); time.sleep(0.4)
# pen: a wave along the bottom
click(29, 527)
# uneven on purpose: spacing, heights, handle length and angle, and pace all differ point to point
pts = [(452, 636, None, 0.42), (611, 566, (676, 552, 0.30), 0.50), (793, 653, (884, 661, 0.42), 0.38),
       (1006, 571, (1068, 557, 0.28), 0.47), (1158, 628, None, 0.40)]
for p in pts:
    move(p[0], p[1], p[3])
    if p[2]: drag(p[2][0], p[2][1], p[2][2], hold=0.08)
    else: click(pause=0.12)
    if p is pts[0]:
        print(color_active(fill_on=False, stroke_on=True, stroke='INK', width=0.05))
time.sleep(0.3); key('Tab'); time.sleep(0.2)
bx('bpy.ops.object.select_all(action="DESELECT")')
move(700, 900, 0.4); time.sleep(1.8)
print(rec_stop())

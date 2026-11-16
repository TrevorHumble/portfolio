from common import *
reset(panel=False)
bx('''ob=import_logo("flatland-mark-small-ink", 3.0, (0, 0), fill=SCARLET)
for p in ob.data.splines[0].bezier_points: p.handle_left_type = p.handle_right_type = 'VECTOR'
print(ob.location[:], [ (round(p.co.x,3), round(p.co.y,3)) for p in ob.data.splines[0].bezier_points])''')
jump(*W(2.4, -1.8)); time.sleep(1)
rec_start('mirror'); time.sleep(0.6)
move(*W(0.6, -0.2), 0.5); key('Tab', pause=0.5)
key('alt+a', pause=0.3)
click(1563, 66, 0.8); time.sleep(0.6)              # Mirror X
click(*W(1.578, 0.354), 0.8); time.sleep(0.3)          # one eave
key('g', pause=0.1); move(*W(2.1, 0.75), 0.9); click(pause=0.3); time.sleep(0.5)
click(*W(0.975, -1.5), 0.7); time.sleep(0.3)         # one foot
key('g', pause=0.1); move(*W(1.35, -1.6), 0.9); click(pause=0.3); time.sleep(0.5)
click(*W(0.0, 1.5), 0.7); time.sleep(0.3)          # the peak stays on the line
key('g', pause=0.1); move(*W(0.5, 1.95), 0.9); click(pause=0.3); time.sleep(0.6)
key('Tab', pause=0.4)
bx('bpy.ops.object.select_all(action="DESELECT")')
move(*W(2.4, -1.8), 0.5); time.sleep(1.5)
print(rec_stop())

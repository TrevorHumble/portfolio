from common import *
reset(panel=True)
bx(open(os.path.join(H, 'clip_scene.py')).read())
jump(1100, 850); time.sleep(1.2)
rec_start('clip'); time.sleep(0.6)
click(1450, 348, 0.7); time.sleep(0.9)           # Make Clipping Path
click(1470, 382, 0.5); time.sleep(0.6)           # Crops:
click(1405, 438, 0.5); time.sleep(1.2)           # Stripes
move(*W(0.3, -0.2), 0.7); key('g', pause=0.1)
move(*W(-1.2, 0.5), 1.0); move(*W(1.6, -0.75), 1.4); move(*W(0.3, -0.2), 0.8); click(pause=0.2)
time.sleep(0.6)
bx('bpy.ops.object.select_all(action="DESELECT")')
move(1100, 850, 0.5); time.sleep(1.5)
print(rec_stop())

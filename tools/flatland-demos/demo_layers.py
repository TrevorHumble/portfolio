from common import *
import sys
PROBE = len(sys.argv) > 1
reset(panel=True)
bx('''a=add_shape("RECTANGLE", -0.9, 0.3, fill=INK, width=2.4, height=2.4); a.flatland_stroke.enabled=False; a.name="Square"
b=add_shape("ELLIPSE", 0.1, -0.2, fill=SCARLET, width=2.4, height=2.4); b.flatland_stroke.enabled=False; b.name="Sun"
c=add_shape("STAR", 1.0, 0.4, fill=PAPER, stroke=INK, width=2.2, height=2.2); c.flatland_stroke.width=0.05; c.name="Star"
bpy.ops.object.select_all(action="DESELECT")''')
jump(1100, 850); time.sleep(1)
if not PROBE: rec_start('layers')
time.sleep(0.5)
# drag the Square row from the bottom of the list to the top: it comes to the front
move(1372, 297, 0.6); time.sleep(0.25); down(); time.sleep(0.3)
move(1374, 280, 0.3); move(1371, 249, 0.7); time.sleep(0.35); up(); time.sleep(1.0)
click(*W(0.0, -1.0), 0.6); time.sleep(0.3)        # Sun on the canvas
xd('keydown', 'shift'); click(*W(1.35, 0.9), 0.5); xd('keyup', 'shift'); time.sleep(0.4)   # and the Star
click(1551, 297, 0.6); time.sleep(1.0)            # group them
click(1340, 275, 0.6); time.sleep(0.6)            # fold the group
move(1395, 275, 0.5); xd('click', '--repeat', 2, '--delay', 80, 1); time.sleep(0.3)  # rename
key('ctrl+a', pause=0.1); typ('Sky', 120); key('Return', pause=0.6)
if PROBE: shot('l2')
bx('bpy.ops.object.select_all(action="DESELECT")'); time.sleep(0.5)
move(1100, 850, 0.6); time.sleep(1.5)
if not PROBE: print(rec_stop())
if PROBE: shot('l3')

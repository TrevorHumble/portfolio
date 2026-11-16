from common import *
reset(panel=False)
bx('''for (x,y,f) in [(-0.75,0.35,SCARLET),(0.75,0.35,INK),(0,-0.85,PAPER)]:
    ob=add_shape("ELLIPSE", x, y, fill=f, stroke=INK, width=2.4, height=2.4)
    ob.flatland_stroke.width=0.04
bpy.ops.object.select_all(action="SELECT")
for o in bpy.data.objects:
    if o.name=="Paper": o.select_set(False)
''')
jump(700, 900); time.sleep(0.8)
rec_start('shape-builder'); time.sleep(0.6)
click(29, 636, 0.6); time.sleep(0.4)
# drag through the top-left lens, the centre and the bottom piece
move(*W(-1.6, 0.9), 0.6)
path_drag([W(-0.9, 0.3), W(0, 0.0), W(0.1, -0.6), W(0, -1.7)], dur=1.8)
time.sleep(0.6); key('Return'); time.sleep(1.5)
bx('''c=ctx_view()
with bpy.context.temp_override(**c):
    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
bpy.ops.object.select_all(action="DESELECT")''')
move(700, 900, 0.5); time.sleep(1.5)
print(rec_stop())
print(bx('print([o.name for o in bpy.data.objects])'))

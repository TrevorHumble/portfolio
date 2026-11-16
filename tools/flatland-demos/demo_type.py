from common import *
reset(panel=True)
jump(700, 900); time.sleep(0.6)
rec_start('type'); time.sleep(0.5)
click(29, 599, 0.5); move(470, 540, 0.6); click(); time.sleep(0.3)
color_active(fill='INK')
bx('''c=ctx_view()
with bpy.context.temp_override(**c):
    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")''')
time.sleep(0.3)
key('Tab'); time.sleep(0.2)
for i in range(4): key('BackSpace', pause=0.06)
typ('Flatland', 140); time.sleep(0.3); key('Tab'); time.sleep(0.6)
click(1551, 285, 0.6); time.sleep(0.8)          # font list
click(1430, 316, 0.4); typ('grav', 140); key('Return'); time.sleep(0.8)
click(1400, 357, 0.5); time.sleep(1.0)          # Gravitas One
click(1420, 372, 0.6); time.sleep(0.8)          # small caps
set_field(1458, 432, '1.2'); time.sleep(0.3)    # spacing
set_field(1458, 525, '0.2'); time.sleep(0.6)    # slant
move(700, 900, 0.5); time.sleep(1.5)
print(rec_stop())
print(bx('ob=bpy.context.object; print(ob.data.body, ob.data.font.name, ob.data.space_character, ob.data.shear)'))

from common import *
reset(panel=True, stroke_open=True)
bx('ob=add_poly([(-3,-1.2),(-1.6,1.2),(-0.2,-1.2),(1.2,1.2),(2.6,-1.2)], fill_enabled=False, stroke_enabled=True, stroke_color=SCARLET, stroke_width=0.04)')
jump(1100, 850); time.sleep(0.6)
rec_start('stroke'); time.sleep(0.5)
set_field(1440, 214, '0.18')                    # width
click(1467, 291, 0.5); time.sleep(0.3)          # round corners
click(1467, 268, 0.4); time.sleep(0.4)          # round caps
# Alt S: Blender's shrink/fatten sets the stroke's width at the selected points
move(*W(-1.1, 0.3), 0.5); key('Tab', pause=0.5); key('alt+a', pause=0.3)
click(*W(-1.6, 1.2), 0.45); time.sleep(0.3)                    # one point: the stroke swells there
move(*W(-1.25, 0.85), 0.35); key('alt+s', pause=0.25); move(*W(-0.85, 0.45), 0.8); time.sleep(0.25); click(pause=0.3); time.sleep(0.6)
key('a', pause=0.4)                                              # every point: the whole stroke grows
move(*W(0.5, -0.24), 0.5); key('alt+s', pause=0.25); move(*W(0.8, -0.3), 0.7); time.sleep(0.25); click(pause=0.3); time.sleep(0.9)
# Ctrl Z puts the width back, so the dashes that follow are easy to read (each selection is an undo
# step in edit mode too, so the two widenings take four presses)
key('ctrl+z', pause=0.25); key('ctrl+z', pause=0.6); key('ctrl+z', pause=0.25); key('ctrl+z', pause=0.8)
print(bx('ob=bpy.context.object; print("radii", [round(p.radius,2) for p in ob.data.splines[0].bezier_points])'))
key('Tab', pause=0.6)
click(1336, 376, 0.5); time.sleep(0.7)          # dashed on
set_field(1413, 399, '0.35')                    # dash
set_field(1526, 399, '0.25')                    # gap
shift_drag(1430, 464, 110, 1.8); time.sleep(0.3) # phase: dashes travel
set_field(1413, 399, '0')                        # dots
time.sleep(0.6)
move(1100, 850, 0.5); time.sleep(1.4)
print(rec_stop())
print(bx('s=bpy.context.object.flatland_stroke; print(s.width, s.dash_1, s.gap_1, s.dash_phase)'))

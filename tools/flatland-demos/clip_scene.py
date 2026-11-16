col = bpy.data.collections.new("Stripes"); bpy.data.collections['Collection'].children.link(col)
lc = bpy.context.view_layer.layer_collection.children['Collection'].children['Stripes']
bpy.context.view_layer.active_layer_collection = lc
for i in range(9):
    y = 1.6 - i * 0.4
    ob = add_shape("RECTANGLE", 0, y, fill=(SCARLET if i % 2 == 0 else INK), width=7.4, height=0.4)
    ob.flatland_stroke.enabled = False; ob.name = "Stripe"
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['Collection']
sun = add_shape("ELLIPSE", 0, 0, fill=PAPER, stroke=INK, width=2.9, height=2.9); sun.flatland_stroke.width = 0.05; sun.name = "Window"
bpy.ops.object.select_all(action="DESELECT"); sun.select_set(True); bpy.context.view_layer.objects.active = sun

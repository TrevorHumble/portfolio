import importlib, os
em = import_logo("flatland-emblem-ink", 2.7, (-2.25, 0.05), fill=SCARLET)
tt = importlib.import_module("bl_ext.user_default.flatland.ops.text_tool_ops")
c = ctx_view()
with bpy.context.temp_override(**c):
    t = tt.place_text(bpy.context, -0.55, -0.3)
t.data.body = "Flatland"; t.name = "Title"
t.data.font = bpy.data.fonts.load(os.path.join(os.environ["FLATLAND_FONT_DIR"], "GravitasOne-Regular.ttf"))
t.data.size = 0.95; t.data.small_caps_scale = 0.75
for ch in t.data.body_format: ch.use_small_caps = True
t.flatland_fill.enabled = True; t.flatland_fill.color = INK
bpy.ops.object.select_all(action="DESELECT")

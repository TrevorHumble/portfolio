"""Build flatland-demo-scenes.blend: one Blender scene per Flatland demo, ready to record by hand.

Run it in Blender 5.2+ with Flatland installed and enabled (a real Flatland, not the
patch_flatland_for_xvfb.py copy):

    blender --python build_scenes.py -- --logos <kit>/logo --fonts <kit>/fonts --out flatland-demo-scenes.blend --quit

Run it with a window (no --background) so the saved file opens with the 3D view filling the window and
the Flatland tab showing; --background works too, with Blender's default layout.

To recolour every scene, change PALETTE below and run it again. Each scene starts exactly where its
take begins; RECORDING.md says what to do in each one.
"""
import os
import sys
import math
import importlib

import bpy
import bmesh
from mathutils import Matrix

# -- the brand palette: change these three and rebuild ------------------------------------------
PALETTE = {
    "ink": "#16161A",
    "paper": "#EFEAE0",
    "accent": "#E05450",     # Scarlet Ibis in brand kit v5
}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


INK, PAPER, ACCENT = (_rgb(PALETTE[k]) for k in ("ink", "paper", "accent"))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def _arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default
LOGOS = _arg("--logos", os.environ.get("FLATLAND_LOGO_DIR", ""))
FONTS = _arg("--fonts", os.environ.get("FLATLAND_FONT_DIR", ""))
OUT = _arg("--out", "flatland-demo-scenes.blend")

FL = "bl_ext.user_default.flatland"
text_tool = importlib.import_module(FL + ".ops.text_tool_ops")
last_style = importlib.import_module(FL + ".ops.last_style")


# -- shared pieces ------------------------------------------------------------------------------

def paper_canvas(scene):
    """The Paper page every scene draws on: a rounded 8 by 4.5 rectangle, unselectable, below the art.
    A mesh, so it is never a Flatland layer and never exports."""
    me = bpy.data.meshes.get("Paper")
    if me is None:
        me = bpy.data.meshes.new("Paper"); bm = bmesh.new(); vs = []
        w, h, r = 8.0, 4.5, 0.12
        for cx, cy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
            for i in range(9):
                a = math.radians(a0 + i * 90 / 8)
                vs.append(bm.verts.new((cx + r * math.cos(a), cy + r * math.sin(a), 0)))
        bm.faces.new(vs); bm.to_mesh(me); bm.free()
        mat = bpy.data.materials.new("Paper"); me.materials.append(mat)
    mat = me.materials[0]
    mat.diffuse_color = (*PAPER, 1)                       # Solid view
    mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()   # Material Preview
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*PAPER, 1); nt.links.new(em.outputs[0], out.inputs[0])
    ob = bpy.data.objects.new("Paper", me); ob.location.z = -0.01; ob.hide_select = True
    scene.collection.objects.link(ob)


def new_scene(name):
    sc = bpy.data.scenes.new(name)
    sc.view_settings.view_transform = "Raw"                # Flatland's neutral view: stored colour is screen colour
    col = bpy.data.collections.new(name.split(" ", 1)[1] + " art")
    sc.collection.children.link(col)
    if bpy.context.window:
        bpy.context.window.scene = sc
    paper_canvas(sc)
    return sc, col


class In:
    """Make `scene` and its art collection the context for Flatland's operators."""
    def __init__(self, scene, col):
        self.scene, self.col = scene, col
    def __enter__(self):
        self.ov = bpy.context.temp_override(scene=self.scene, view_layer=self.scene.view_layers[0])
        self.ov.__enter__()
        vl = self.scene.view_layers[0]
        vl.active_layer_collection = vl.layer_collection.children[self.col.name]
        return self
    def __exit__(self, *a):
        self.ov.__exit__(*a)


def style(ob, fill=None, stroke=None, width=None):
    if fill is None:
        ob.flatland_fill.enabled = False
    else:
        ob.flatland_fill.enabled = True; ob.flatland_fill.color = fill
    if stroke is None:
        ob.flatland_stroke.enabled = False
    else:
        ob.flatland_stroke.enabled = True; ob.flatland_stroke.color = stroke
        if width: ob.flatland_stroke.width = width
    return ob


def shape(kind, x, y, w, h, name, **st):
    bpy.ops.flatland.primitive_add(shape=kind, center_x=x, center_y=y, width=w, height=h)
    ob = bpy.context.view_layer.objects.active; ob.name = name
    return style(ob, **st)


def poly(pts, name, closed=False, **st):
    bpy.ops.flatland.polyline_add(pts_data=";".join("%r,%r" % p for p in pts), closed=closed)
    ob = bpy.context.view_layer.objects.active; ob.name = name
    return style(ob, **st)


def logo(svg, height, loc, name, fill, straight=False):
    """A brand-kit logo SVG, imported as a plain Blender curve (not a Flatland shape)."""
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=os.path.join(LOGOS, svg + ".svg"))
    new = [o for o in bpy.data.objects if o not in before]
    ob = new[0]
    for o in new: o.data.materials.clear()
    for c in list(ob.users_collection): c.objects.unlink(ob)
    for c in list(bpy.data.collections):
        if c.name.startswith(svg) and not c.objects: bpy.data.collections.remove(c)
    bpy.context.view_layer.active_layer_collection.collection.objects.link(ob)
    # size and centre from the curve's own points (an object's bound box is stale until a redraw)
    pts = [p.co for sp in ob.data.splines for p in sp.bezier_points]
    xs, ys = [v.x for v in pts], [v.y for v in pts]
    s = height / (max(ys) - min(ys))
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    ob.data.transform(Matrix.Scale(s, 4) @ Matrix.Translation((-cx, -cy, 0)))
    ob.location = (loc[0], loc[1], 0)
    if straight:
        for sp in ob.data.splines:
            for p in sp.bezier_points: p.handle_left_type = p.handle_right_type = "VECTOR"
    ob.name = name
    return style(ob, fill=fill)


def prime_last_style(scene, fill=None, stroke=None, width=None):
    """Set the style a new shape is born with in this scene (Flatland remembers it per scene)."""
    tmp = shape("RECTANGLE", 0, 0, 1, 1, "_prime", fill=fill, stroke=stroke, width=width)
    last_style.capture(scene, tmp)
    bpy.data.objects.remove(tmp)


def deselect(scene):
    for o in scene.objects: o.select_set(False)


# -- the scenes, in the order the Flatland page shows them ----------------------------------------

def s01_shapes():
    sc, col = new_scene("01 Shapes and pen")
    with In(sc, col): prime_last_style(sc, fill=INK)


def s02_type():
    sc, col = new_scene("02 Type")
    with In(sc, col): prime_last_style(sc, fill=INK)


def s03_gradient():
    sc, col = new_scene("03 Gradient")
    with In(sc, col):
        ob = shape("RECTANGLE", -0.6, 0, 4.5, 3.2, "Card", fill=ACCENT)
        with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob]):
            bpy.ops.flatland.set_gradient_paint(slot="fill", paint="LINEAR")
            r = ob.data.materials[0].node_tree.nodes["flatland_ramp_fill"].color_ramp
            r.elements[1].color = (*INK, 1)
            e = r.elements.new(0.5); e.color = (*PAPER, 1)
            bpy.ops.flatland.set_gradient_paint(slot="fill", paint="FLAT")


def s04_strokes():
    sc, col = new_scene("04 Strokes")
    with In(sc, col):
        poly([(-3, -1.2), (-1.6, 1.2), (-0.2, -1.2), (1.2, 1.2), (2.6, -1.2)], "Zigzag", stroke=ACCENT, width=0.04)


def s05_layers():
    sc, col = new_scene("05 Layers")
    with In(sc, col):
        shape("RECTANGLE", -0.9, 0.3, 2.4, 2.4, "Square", fill=INK)
        shape("ELLIPSE", 0.1, -0.2, 2.4, 2.4, "Sun", fill=ACCENT)
        shape("STAR", 1.0, 0.4, 2.2, 2.2, "Star", fill=PAPER, stroke=INK, width=0.05)


def s06_clipping():
    sc, col = new_scene("06 Clipping paths")
    stripes = bpy.data.collections.new("Stripes"); col.children.link(stripes)
    with In(sc, col):
        vl = sc.view_layers[0]
        vl.active_layer_collection = vl.layer_collection.children[col.name].children["Stripes"]
        for i in range(9):
            shape("RECTANGLE", 0, 1.6 - i * 0.4, 7.4, 0.4, "Stripe", fill=(ACCENT if i % 2 == 0 else INK))
        vl.active_layer_collection = vl.layer_collection.children[col.name]
        shape("ELLIPSE", 0, 0, 2.9, 2.9, "Window", fill=PAPER, stroke=INK, width=0.05)


def s07_shape_builder():
    sc, col = new_scene("07 Shape Builder")
    with In(sc, col):
        for (x, y, f, n) in [(-0.75, 0.35, ACCENT, "Left"), (0.75, 0.35, INK, "Right"), (0, -0.85, PAPER, "Bottom")]:
            shape("ELLIPSE", x, y, 2.4, 2.4, n, fill=f, stroke=INK, width=0.04)


def s08_pathfinder():
    sc, col = new_scene("08 Pathfinder")
    with In(sc, col):
        for i, x in enumerate([-2.85, -0.95, 0.95, 2.85]):
            shape("RECTANGLE", x - 0.22, 0.2, 1.1, 1.1, "Square %d" % (i + 1), fill=INK)
            shape("ELLIPSE", x + 0.22, -0.2, 1.1, 1.1, "Circle %d" % (i + 1), fill=ACCENT)


def s09_bevel():
    sc, col = new_scene("09 Bevel")
    with In(sc, col):
        logo("flatland-mark-small-ink", 3.0, (0, 0), "House", INK)


def s10_mirror():
    sc, col = new_scene("10 Mirror editing")
    with In(sc, col):
        logo("flatland-mark-small-ink", 3.0, (0, 0), "House", ACCENT, straight=True)


def s11_export():
    sc, col = new_scene("11 Export")
    with In(sc, col):
        logo("flatland-emblem-ink", 2.7, (-2.25, 0.05), "Emblem", ACCENT)
        t = text_tool.place_text(bpy.context, -0.55, -0.3)
        font = bpy.data.fonts.load(os.path.join(FONTS, "GravitasOne-Regular.ttf"), check_existing=True)
        font.pack()                                       # travels inside the .blend
        # no build machine path saved in the file: Blender keeps the path in a fixed buffer, so fill
        # it first, or the end of the old path survives after the new one
        font.filepath = "/" * 1000
        font.filepath = "//GravitasOne-Regular.ttf"
        t.data.body = "Flatland"; t.name = "Title"; t.data.font = font
        t.data.size = 0.95; t.data.small_caps_scale = 0.75
        for ch in t.data.body_format: ch.use_small_caps = True
        style(t, fill=INK)


def setup_view():
    """Every scene is framed the same way: top orthographic, the Paper page centred, no grid."""
    win = bpy.context.window
    if win:
        # run with a window (no --background): the 3D view fills the window, as in the GIFs
        area = next(a for a in win.screen.areas if a.type == "VIEW_3D")
        with bpy.context.temp_override(window=win, area=area, region=next(r for r in area.regions if r.type == "WINDOW")):
            if not win.screen.show_fullscreen:
                bpy.ops.screen.screen_full_area()
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            sp = area.spaces[0]; r3 = sp.region_3d
            r3.view_perspective = "ORTHO"
            r3.view_rotation = (1, 0, 0, 0)
            r3.view_location = (0, 0, 0); r3.view_distance = 10.7
            ov = sp.overlay
            ov.show_floor = False; ov.show_axis_x = False; ov.show_axis_y = False; ov.show_cursor = False
            sp.shading.type = "SOLID"; sp.shading.light = "FLAT"; sp.shading.color_type = "MATERIAL"
            sp.show_region_ui = True
            for r in area.regions:
                if r.type == "UI":
                    try:
                        r.active_panel_category = "Flatland"
                    except AttributeError:
                        pass        # read-only before the sidebar has drawn; click the Flatland tab once


def notes():
    t = bpy.data.texts.get("RECORDING NOTES") or bpy.data.texts.new("RECORDING NOTES")
    t.clear()
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "RECORDING.md")
    t.write(open(path).read() if os.path.exists(path) else "See tools/flatland-demos/RECORDING.md")


def main():
    for sc in list(bpy.data.scenes):
        if sc.name[:2].isdigit():
            bpy.data.scenes.remove(sc)
    for fn in (s01_shapes, s02_type, s03_gradient, s04_strokes, s05_layers, s06_clipping,
               s07_shape_builder, s08_pathfinder, s09_bevel, s10_mirror, s11_export):
        fn()
    for sc in list(bpy.data.scenes):
        if not sc.name[:2].isdigit():
            bpy.data.scenes.remove(sc)                    # the startup file's empty "Scene"
    for sc in bpy.data.scenes:
        deselect(sc)
    setup_view()
    notes()
    if bpy.context.window:
        bpy.context.window.scene = bpy.data.scenes["01 Shapes and pen"]
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT))
    print("saved", os.path.abspath(OUT), "scenes:", [s.name for s in bpy.data.scenes])
    if "--quit" in argv:
        bpy.ops.wm.quit_blender()


main()

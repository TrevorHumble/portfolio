import bpy, mathutils, os
INK=(0x16/255,0x16/255,0x1A/255); PAPER=(0xEF/255,0xEA/255,0xE0/255); SCARLET=(0xE0/255,0x54/255,0x50/255)
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)
_sc = bpy.context.scene
if '_flatland_last_style' in _sc: del _sc['_flatland_last_style']
_ng = bpy.data.node_groups.get('flatland_last_style')
if _ng: bpy.data.node_groups.remove(_ng)
for _c in list(bpy.data.collections):
    if _c.name != 'Collection': bpy.data.collections.remove(_c)
if 'Collection' not in bpy.data.collections:
    _sc.collection.children.link(bpy.data.collections.new('Collection'))
_col = bpy.data.collections['Collection']
if _col.name not in _sc.collection.children: _sc.collection.children.link(_col)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['Collection']
_ts=_sc.tool_settings; _ts.use_transform_data_origin=False
c = ctx_view()
with bpy.context.temp_override(**c):
    if not c['screen'].show_fullscreen:
        bpy.ops.screen.screen_full_area()
c = ctx_view()
sp = c['area'].spaces[0]
ov = sp.overlay
ov.show_floor=False; ov.show_axis_x=False; ov.show_axis_y=False; ov.show_axis_z=False; ov.show_cursor=False
ov.show_text=True; ov.show_stats=False
sp.shading.type='SOLID'
r3 = sp.region_3d
r3.view_perspective='ORTHO'
r3.view_rotation = mathutils.Quaternion((1,0,0,0))
r3.view_location=(0,0,0); r3.view_distance=10.7
th = bpy.context.preferences.themes[0]
th.view_3d.space.gradients.high_gradient=(0.045,0.045,0.045)
th.view_3d.space.gradients.background_type='SINGLE_COLOR'
print(sp.shading.light, sp.shading.color_type, c['area'].width, c['area'].height)
sp.shading.light='FLAT'
bpy.context.scene.view_settings.view_transform='Raw'
import bmesh, math
def rounded_rect(name, w, h, r, color, z):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); vs=[]
    for cx,cy,a0 in ((w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)):
        for i in range(9):
            a=math.radians(a0+i*90/8); vs.append(bm.verts.new((cx+r*math.cos(a), cy+r*math.sin(a), 0)))
    bm.faces.new(vs); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new(name); mat.diffuse_color=(*[(v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4) for v in color],1); me.materials.append(mat)
    ob.location.z = z; ob.hide_select=True
    return ob
rounded_rect("Paper", 8.0, 4.5, 0.12, PAPER, -0.01)
def region_xy(co):
    from bpy_extras.view3d_utils import location_3d_to_region_2d
    c = ctx_view(); p = location_3d_to_region_2d(c['region'], c['region'].data, co)
    win_h = c['window'].height
    return (round(c['region'].x + p.x), round(win_h - (c['region'].y + p.y)))
r = c['region']; print('region', r.x, r.y, r.width, r.height, 'win', c['window'].height, 'area', c['area'].y, c['area'].height)
def show_panel(on=True):
    c = ctx_view(); c['area'].spaces[0].show_region_ui = on
    for r in c['area'].regions:
        if r.type == 'UI': r.active_panel_category = 'Flatland'
def add_shape(shape, x, y, fill=None, stroke=None, **kw):
    c = ctx_view()
    with bpy.context.temp_override(**c):
        bpy.ops.flatland.primitive_add(shape=shape, center_x=x, center_y=y, **kw)
    ob = bpy.context.object
    if fill is not None: ob.flatland_fill.color = fill
    if stroke is not None: ob.flatland_stroke.color = stroke
    return ob
def add_poly(pts, closed=False, **style):
    c = ctx_view()
    with bpy.context.temp_override(**c):
        bpy.ops.flatland.polyline_add(pts_data=";".join("%r,%r" % p for p in pts), closed=closed)
    ob = bpy.context.object
    for k, v in style.items():
        tgt, _, attr = k.partition('_')
        setattr(getattr(ob, 'flatland_' + tgt), attr, v)
    return ob
def native_curve(name, pts, loc=(0,0,0)):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1); sp.use_cyclic_u = True
    for bp, (x, y) in zip(sp.bezier_points, pts):
        bp.co = (x, y, 0); bp.handle_left_type = bp.handle_right_type = 'VECTOR'
    ob = bpy.data.objects.new(name, cu); ob.location = loc
    bpy.data.collections['Collection'].objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
    return ob
def _dec(v): return v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4
def emission_fix():
    # recording-only: this machine's viewport encodes to sRGB twice, so decode Flatland's emission colours once
    for m in bpy.data.materials:
        if not m.use_nodes or m.name == 'Paper': continue
        nt = m.node_tree
        for em in [n for n in nt.nodes if n.bl_idname == 'ShaderNodeEmission']:
            sock = em.inputs['Color']
            if sock.is_linked:
                src = sock.links[0].from_socket
                if src.node.bl_idname == 'ShaderNodeGamma' and src.node.name.startswith('_recfix'): continue
                g = nt.nodes.new('ShaderNodeGamma'); g.name = '_recfix'; g.inputs['Gamma'].default_value = 2.2
                g.location = (em.location.x - 150, em.location.y - 200)
                nt.links.new(src, g.inputs['Color']); nt.links.new(g.outputs['Color'], sock)
            else:
                key = '_recfix_val'
                cur = tuple(sock.default_value)
                if em.get(key) is not None and tuple(em[key]) == tuple(round(x, 6) for x in cur): continue
                new = tuple(_dec(x) for x in cur[:3]) + cur[3:]
                sock.default_value = new; em[key] = [round(x, 6) for x in new]
    return 0.05
def paper_emission():
    m = bpy.data.materials['Paper']; m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*PAPER, 1); nt.links.new(em.outputs[0], out.inputs[0])
LOGO_DIR = os.environ.get('FLATLAND_LOGO_DIR', '')
def import_logo(name, height, loc, fill=None):
    """Import a brand-kit logo SVG as a plain Blender curve, sized to `height` and centred on `loc`."""
    import os
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=os.path.join(LOGO_DIR, name + '.svg'))
    new = [o for o in bpy.data.objects if o not in before]
    ob = new[0]
    for o in new: o.data.materials.clear()
    for c in list(ob.users_collection): c.objects.unlink(ob)
    bpy.data.collections['Collection'].objects.link(ob)
    for c in list(bpy.data.collections):
        if c.name != 'Collection' and not c.objects and not c.children: bpy.data.collections.remove(c)
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
    s = height / ob.dimensions.y
    ob.scale = (s, s, s)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    ob.location = (loc[0], loc[1], 0.0)
    ob.name = name
    if fill is not None:
        ob.flatland_fill.enabled = True; ob.flatland_fill.color = fill
    ob.flatland_stroke.enabled = False
    return ob

from common import *
def wait_compile(t=60):
    for i in range(t):
        time.sleep(1)
        if 'Compiling' not in bx('import bpy\nprint(bpy.app.is_job_running("SHADER_COMPILATION"))').replace('False', ''):
            if i > 2: break
reset(panel=True, fill_open=True)
bx('''paper_emission()
c=ctx_view(); c["area"].spaces[0].shading.type="MATERIAL"
ob=add_shape("RECTANGLE", -0.6, 0, fill=SCARLET, width=4.5, height=3.2); ob.flatland_stroke.enabled=False''')
time.sleep(1)
click(1442, 154, 0.2); time.sleep(2)
bx("""ob=bpy.context.object
r=ob.data.materials[0].node_tree.nodes["flatland_ramp_fill"].color_ramp
r.elements[1].color=(*INK,1)
e=r.elements.new(0.5); e.color=(*PAPER,1)
""")
time.sleep(2); click(1366, 154, 0.2); time.sleep(2)
# warm up the shader variants so nothing compiles on camera
for x in (1442, 1517, 1442, 1366):
    click(x, 154, 0.2); time.sleep(3); 
    for i in range(90):
        time.sleep(1)
        if bx('print(bpy.app.is_job_running("SHADER_COMPILATION"))').strip() == 'False': break
jump(1100, 850); time.sleep(1); shot('gpre')
rec_start('gradient'); time.sleep(0.6)
click(1442, 154, 0.6); time.sleep(1.2)                          # linear
move(971, 508, 0.6); time.sleep(0.2); drag(900, 340, 1.0); time.sleep(0.8)   # turn it by its handle
move(1443, 207, 0.6); time.sleep(0.2); drag(1385, 207, 0.8); time.sleep(0.8) # slide the middle colour
click(1517, 154, 0.6); time.sleep(1.5)                          # radial
move(1100, 850, 0.5); time.sleep(1.5)
print(rec_stop())

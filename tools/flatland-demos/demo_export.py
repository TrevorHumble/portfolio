from common import *
reset(panel=True)
bx(open(os.path.join(H, 'export_scene.py')).read())
jump(1100, 850); time.sleep(1.5)
rec_start('export'); time.sleep(0.8)
move(1540, 702, 1.0); time.sleep(0.3); click(pause=0.2); time.sleep(1.4)
print(rec_stop())
print(bx('''import glob, os
fs = sorted(glob.glob(os.path.join(bpy.app.tempdir, "flatland-preview-*.html")), key=os.path.getmtime)
print(fs[-1] if fs else "NONE")'''))

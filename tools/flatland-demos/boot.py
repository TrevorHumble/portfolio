import bpy, os, traceback, io, contextlib
H = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.environ['HDIR']
CMD = os.path.join(H, 'cmd.py'); OUT = os.path.join(H, 'out.txt')
G = {'bpy': bpy}
def ctx_view():
    for w in bpy.context.window_manager.windows:
        for a in w.screen.areas:
            if a.type == 'VIEW_3D':
                r = [r for r in a.regions if r.type == 'WINDOW'][0]
                return dict(window=w, area=a, region=r, screen=w.screen)
G['ctx_view'] = ctx_view
def poll():
    if os.path.exists(CMD):
        src = open(CMD).read(); os.remove(CMD)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(src, G)
        except Exception:
            buf.write(traceback.format_exc())
        with open(OUT + '.tmp', 'w') as f: f.write(buf.getvalue())
        os.replace(OUT + '.tmp', OUT)
    return 0.05
bpy.app.timers.register(poll, first_interval=1.0, persistent=True)
open(os.path.join(H,"ready"),"w").close()

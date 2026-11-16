import subprocess, time, os, json, signal, math, random
H = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, DISPLAY=os.environ.get('DISPLAY', ':99'))
def bx(code):
    return subprocess.run([os.path.join(H, 'bx'), code], capture_output=True, text=True, env=ENV).stdout
_trace = []                    # (wall time, x, y) of every cursor move while recording
def xd(*a):
    subprocess.run(['xdotool', *map(str, a)], env=ENV)
    if a and a[0] == 'mousemove' and _rec.get('p'):
        _trace.append((time.time(), int(a[1]), int(a[2])))
_pos = [800, 500]
SCREEN = (1600, 1012)
RATE = 60                      # cursor samples per second


def _min_jerk(t):
    """Minimum-jerk position for t in 0..1: a smooth bell-shaped speed curve (Flash and Hogan)."""
    return t * t * t * (10 - 15 * t + 6 * t * t)


def _skew(t, k=0.8):
    """Warp time so the speed peaks a little before the middle, as real reaches do."""
    return t ** k


def _bezier(p0, c, p1, u):
    a = (1 - u) * (1 - u); b = 2 * (1 - u) * u; d = u * u
    return (a * p0[0] + b * c[0] + d * p1[0], a * p0[1] + b * c[1] + d * p1[1])


def _control(x0, y0, x1, y1, rng, bend):
    """The arc's control point: pushed to one side of the midpoint by a share of the distance, so the
    path bows 3 to 5 percent; never zero, so no move is a straight line."""
    dx, dy = x1 - x0, y1 - y0
    dist = max(1e-6, math.hypot(dx, dy))
    side = 1 if rng.random() < 0.5 else -1
    off = max(2.0, rng.uniform(*bend) * dist) * side
    nx, ny = -dy / dist, dx / dist
    k = rng.uniform(0.45, 0.55)
    return (x0 + dx * k + nx * off, y0 + dy * k + ny * off)


def _leg(x0, y0, x1, y1, dur, rng, bend=(0.06, 0.10), c=None):
    """One curved stroke from (x0, y0) to (x1, y1) taking `dur` seconds (HUMAN-MOTION.md)."""
    if math.hypot(x1 - x0, y1 - y0) < 1:
        return
    if c is None:
        c = _control(x0, y0, x1, y1, rng, bend)
    n = max(2, int(dur * RATE))
    last = None
    for i in range(1, n + 1):
        u = _min_jerk(_skew(i / n))
        x, y = _bezier((x0, y0), c, (x1, y1), u)
        p = (min(SCREEN[0] - 1, max(0, round(x))), min(SCREEN[1] - 1, max(0, round(y))))
        if p != last:
            xd('mousemove', *p); last = p
        time.sleep(dur / n)


def move(x, y, dur=0.4, steps=None):
    """Move the cursor the way a hand does (HUMAN-MOTION.md): never a straight line, a speed that ramps
    up, peaks early and settles, a long reach that carries on past the target in the direction it was
    travelling and comes back, and a short stop that creeps the last pixels. Seeded by the endpoints,
    so a rerun records the same take."""
    x0, y0 = _pos
    dist = math.hypot(x - x0, y - y0)
    rng = random.Random(hash((round(x0), round(y0), round(x), round(y))) & 0xffffffff)
    if dist < 1:
        xd('mousemove', round(x), round(y)); _pos[:] = [x, y]; return
    c = _control(x0, y0, x, y, rng, (0.06, 0.10))
    # the direction the hand is travelling as it arrives: the arc's tangent at the target
    tx, ty = x - c[0], y - c[1]
    tl = math.hypot(tx, ty) or 1.0
    tx, ty = tx / tl, ty / tl
    if dist > 260 and dur >= 0.3:
        # carry on 1 to 2 percent past along that heading (1 in 8 goes 3 percent), then come back
        over = (0.03 if rng.random() < 1 / 8 else rng.uniform(0.01, 0.02)) * dist
        wob = rng.uniform(-0.3, 0.3) * over
        ox, oy = x + tx * over - ty * wob, y + ty * over + tx * wob
        fix = rng.uniform(0.1, 0.15)
        # keep the same arc, stretched to the overshoot point, so the heading does not change
        c2 = (c[0] + (ox - x) * 0.5, c[1] + (oy - y) * 0.5)
        _leg(x0, y0, ox, oy, max(0.1, dur - fix), rng, c=c2)
        _leg(ox, oy, x, y, fix, rng, bend=(0.1, 0.25))
    elif dist > 30 and rng.random() < 0.7:
        # stop 1 to 3 px short along the heading, then creep in
        short = rng.uniform(1, 3)
        sx, sy = x - tx * short, y - ty * short
        _leg(x0, y0, sx, sy, dur * 0.9, rng, c=c)
        _leg(sx, sy, x, y, max(0.06, dur * 0.1), rng, bend=(0.2, 0.4))
    else:
        _leg(x0, y0, x, y, dur, rng, c=c)
    xd('mousemove', round(x), round(y))
    _pos[:] = [x, y]


def jump(x, y):
    xd('mousemove', x, y); _pos[:] = [x, y]
def down(b=1): xd('mousedown', b)
def up(b=1): xd('mouseup', b)
def click(x=None, y=None, dur=0.4, b=1, pause=0.15):
    if x is not None: move(x, y, dur)
    time.sleep(pause); xd('click', b); time.sleep(pause)
def drag(x, y, dur=0.6, b=1, hold=0.1):
    down(b); time.sleep(hold); move(x, y, dur); time.sleep(hold); up(b)
def path_drag(pts, dur=1.0, b=1):
    down(b); time.sleep(0.08)
    seg = dur / max(1, len(pts))
    for p in pts: move(*p, dur=seg, steps=max(2, int(seg * 40)))
    time.sleep(0.08); up(b)
def key(*k, pause=0.2):
    xd('key', *k); time.sleep(pause)
def typ(s, delay=90):
    xd('type', '--delay', delay, s)
def w2s(x, y, z=0.0):
    out = bx('print(*region_xy((%r,%r,%r)))' % (x, y, z)).split()
    return int(out[0]), int(out[1])
_rec = {}
def rec_start(name):
    out = os.path.join(H, 'rec', name + '.mkv'); os.makedirs(os.path.dirname(out), exist_ok=True)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'x11grab', '-draw_mouse', '0', '-framerate', '30',
                          '-video_size', '1600x934', '-i', ':99+0,52', '-copyts', '-c:v', 'libx264rgb', '-crf', '0',
                          '-preset', 'ultrafast', out], stdin=subprocess.PIPE, env=ENV)
    _trace.clear(); _trace.append((time.time() - 5, round(_pos[0]), round(_pos[1])))
    _rec['p'] = p; _rec['out'] = out; time.sleep(0.8)
def rec_stop():
    time.sleep(0.3); p = _rec['p']; p.stdin.write(b'q'); p.stdin.flush(); p.wait(); _rec['p'] = None
    json.dump(_trace, open(_rec['out'].replace('.mkv', '.trace.json'), 'w'))
    return _rec['out']
def shot(name='s'):
    out = os.path.join(H, name + '.png'); subprocess.run(['import', '-window', 'root', out], env=ENV); return out

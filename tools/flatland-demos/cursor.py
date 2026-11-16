"""Draw a standard arrow cursor onto a screen recording.

The recorder captures with the system cursor hidden (Xvfb only has the bare X11 'X') and logs every
mouse position with its wall-clock time (drv.py). This draws a familiar white arrow with a black
outline at each logged position, frame by frame, so every GIF shows the same normal cursor.
Usage: python3 cursor.py in.mkv in.trace.json out.mkv
"""
import bisect, json, subprocess, sys
from PIL import Image, ImageDraw

W, H, TOP = 1600, 934, 52          # capture size and the capture's offset from the top of the screen
SCALE = 2                          # the capture is twice the GIF's size

def arrow():
    pts = [(0, 0), (0, 16), (4, 12), (7, 19), (9, 18), (6, 11), (11, 11)]
    big = [(x * SCALE * 4 + 6, y * SCALE * 4 + 6) for x, y in pts]
    im = Image.new('RGBA', (12 * SCALE * 4 + 16, 20 * SCALE * 4 + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon(big, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=SCALE * 4)
    im = im.resize((im.width // 4, im.height // 4), Image.LANCZOS)       # smooth edges
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 60), (2, 3), im.split()[3])
    out = Image.alpha_composite(shadow, im)
    return out, (6 // 4, 6 // 4)

def main(src, trace, dst):
    tr = json.load(open(trace))
    times = [t for t, _, _ in tr]
    pts = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'packet=pts_time',
                          '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.split()
    pts = sorted(float(p) for p in pts if p and p != 'N/A')
    cur, hot = arrow()
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H),
                            '-r', '30', '-i', '-', '-c:v', 'libx264rgb', '-crf', '0', '-preset', 'ultrafast', dst],
                           stdin=subprocess.PIPE)
    i = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = pts[min(i, len(pts) - 1)]
        k = bisect.bisect_right(times, t) - 1
        im = Image.frombytes('RGB', (W, H), buf)
        if k >= 0:
            _, x, y = tr[k]
            im.paste(cur, (int(x) - hot[0], int(y) - TOP - hot[1]), cur)
        enc.stdin.write(im.tobytes())
        i += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print('cursor drawn on', i, 'frames')

if __name__ == '__main__':
    main(*sys.argv[1:4])

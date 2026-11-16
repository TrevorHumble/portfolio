"""Recording-only: the patched add-on writes sRGB-decoded colours into the export; put the brand hex back."""
import re, sys
BRAND = {'16161a': (22, 22, 26), 'efeae0': (239, 234, 224), 'e05450': (224, 84, 80)}
def dec(v):
    v /= 255
    return (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) * 255
p = sys.argv[1]; s = open(p).read()
def fix(m):
    h = m.group(2).lower(); c = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    best = min(BRAND, key=lambda k: sum((dec(a) - b) ** 2 for a, b in zip(BRAND[k], c)))
    return m.group(1) + best
s = re.sub(r'((?:fill|stroke)="#)([0-9a-fA-F]{6})', fix, s)
open(p, 'w').write(s); print(sorted(set(re.findall(r'(?:fill|stroke)="#[0-9a-f]{6}', s))))

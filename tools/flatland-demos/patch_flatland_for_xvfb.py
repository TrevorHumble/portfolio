"""Recording-only patch for a COPY of the Flatland add-on, never the repo itself.

Under Xvfb with Mesa's software renderer, Blender's Solid viewport encodes colours to sRGB a second
time, so Ink, Paper and Scarlet Ibis come out too light (a real GPU shows them true). This decodes
the colour Flatland mirrors into each material's Solid-view colour, so the recording matches what
the owner sees. Side effect: an export from the patched copy carries the decoded colours, which
fix_preview.py puts back. Usage: python3 patch_flatland_for_xvfb.py <copy>/flatland
"""
import sys, os
HELPER = ("\ndef _rec(c):\n    f=lambda v: v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4\n"
          "    c=tuple(c); import array; return tuple(array.array('f', [f(v) for v in c[:3]]+list(c[3:])))\n")
EDITS = {
    'ops/stroke_ops.py': [("    if any(abs(a - b) > 1e-6 for a, b in zip(mat.diffuse_color, colour)):",
                           "    colour = _rec(colour)\n    if any(abs(a - b) > 1e-6 for a, b in zip(mat.diffuse_color, colour)):")],
    'ops/fill_ops.py': [("mat.diffuse_color = colour", "mat.diffuse_color = _rec(colour)")],
    'ops/gradient_ops.py': [("        if tuple(mat.diffuse_color) != flat:", "        flat = _rec(flat)\n        if tuple(mat.diffuse_color) != flat:"),
                            ("    if tuple(mat.diffuse_color) != first:", "    first = _rec(first)\n    if tuple(mat.diffuse_color) != first:")],
}
root = sys.argv[1]
for rel, subs in EDITS.items():
    p = os.path.join(root, rel); s = open(p).read()
    for a, b in subs:
        if a not in s: sys.exit("patch_flatland_for_xvfb: %s no longer has %r" % (rel, a))
        s = s.replace(a, b)
    open(p, 'w').write(s + HELPER)
print("patched", root)

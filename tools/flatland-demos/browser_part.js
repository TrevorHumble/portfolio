const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const dir = process.argv[2], out = process.argv[3];
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 934 } });
  await p.goto('file://' + path.join(dir, 'preview.html'));
  await p.addStyleTag({ content: `
    body { margin: 0; background:#fff; }
           display: flex; align-items: center; padding: 0 20px; gap: 14px; font: 15px system-ui, sans-serif; color: #444; }
    body > svg { width: 1520px !important; max-width: none !important; max-height: none !important; height: auto !important; }
    #cur { position: fixed; width: 18px; height: 28px; pointer-events: none; z-index: 9; }
    #cur .ib { position:absolute; left:8px; top:-4px; width:3px; height:36px; background:#111; box-shadow:0 0 0 1px #fff; }
    #cur .ib::before, #cur .ib::after { content:''; position:absolute; left:-5px; width:13px; height:3px; background:#111; box-shadow:0 0 0 1px #fff; }
    #cur .ib::before { top:0 } #cur .ib::after { bottom:0 }
  `});
  await p.evaluate(() => {
    const c = document.createElement('div'); c.id = 'cur';
    c.innerHTML = '<div class="ib"></div>';
    document.body.append(c);
  });
  await p.evaluate(() => {   // zoom in: the artwork fills the frame
    const v = document.querySelector('svg');
    Object.assign(v.style, { width: '1480px', height: 'auto', maxWidth: 'none', maxHeight: 'none' });
  });
  const r = await p.evaluate(() => { const t = document.querySelector('text'); const b = t.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}; });
  let n = 0;
  const shot = async () => { await p.screenshot({ path: path.join(out, String(n++).padStart(4, '0') + '.png') }); };
  const cur = async (x, y) => { await p.evaluate(([x, y]) => { const c = document.getElementById('cur'); c.style.left = (x - 9) + 'px'; c.style.top = (y - 14) + 'px'; }, [x, y]); };
  const y = r.y + r.h * 0.55, x0 = r.x - 6, x1 = r.x + r.w + 6;
  await cur(x1 + 120, y + 160);
  for (let i = 0; i < 14; i++) await shot();                // hold on the page
  for (let i = 1; i <= 8; i++) { await cur(x1 + 120 - (x1 + 120 - x0) * i / 8, y + 160 - 160 * i / 8); await shot(); }
  await p.mouse.move(x0, y); await p.mouse.down();
  for (let i = 1; i <= 12; i++) { const x = x0 + (x1 - x0) * i / 12; await p.mouse.move(x, y); await cur(x, y); await shot(); }
  await p.mouse.up();
  for (let i = 0; i < 18; i++) await shot();                // hold with the word selected
  console.log(JSON.stringify(r), n);
  await b.close();
})();

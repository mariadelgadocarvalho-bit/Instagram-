// Uso: node tools/export.js <pasta_do_post> [preview|final]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const mode = process.argv[3] || 'preview';
  const scale = mode === 'final' ? 1080 / 420 : 1;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1780, height: 1200 }, deviceScaleFactor: scale });
  await page.goto('file://' + path.join(dir, 'carousel.html'));
  await page.evaluate(() => document.fonts.ready);
  if (mode === 'final') {
    const slides = await page.$$('.slide');
    for (let i = 0; i < slides.length; i++) {
      await slides[i].screenshot({ path: path.join(dir, `slide_${i + 1}.jpg`), type: 'jpeg', quality: 92 });
    }
    console.log(`${slides.length} slides exportados`);
  } else {
    await page.locator('.grid').screenshot({ path: path.join(dir, 'preview.png') });
    console.log('preview.png');
  }
  await browser.close();
})();

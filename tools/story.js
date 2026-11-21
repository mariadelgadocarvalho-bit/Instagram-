// Uso: node tools/story.js <pasta_do_post> "<pergunta A ou B>"
// Gera story.jpg (1080x1920): slide 1 em cartão + faixa "NOVO POST" + pergunta.
// Texto mantido fora dos 250 px de cima e de baixo.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const pergunta = process.argv[3] || 'Qual é a próxima versão? A ou B';
  const fonts = 'file://' + path.resolve(__dirname, '../assets/fonts');
  const browser = await chromium.launch();
  // 1. slide 1 em alta resolução
  const p1 = await browser.newPage({ viewport: { width: 1780, height: 1200 }, deviceScaleFactor: 760 / 420 });
  await p1.goto('file://' + path.join(dir, 'carousel.html'));
  await p1.evaluate(() => document.fonts.ready);
  const card = path.join(dir, 'story_card.png');
  await p1.locator('#s1').screenshot({ path: card });
  // 2. composição da Story
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Bricolage';src:url('${fonts}/Bricolage.woff2') format('woff2');font-weight:200 800}
@font-face{font-family:'Inter';src:url('${fonts}/Inter.woff2') format('woff2');font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#FFFFFF;font-family:'Inter';color:#2B2118;position:relative;overflow:hidden}
.card{position:absolute;left:160px;top:270px;width:760px;height:950px;border-radius:36px;overflow:hidden;box-shadow:0 24px 60px rgba(43,33,24,.22);transform:rotate(-2deg)}
.card img{width:100%;height:100%;display:block}
.band{position:absolute;left:0;right:0;top:1290px;background:#E4572E;color:#fff;font-family:'Bricolage';font-weight:800;font-size:50px;letter-spacing:-.5px;text-align:center;padding:30px 0;display:flex;justify-content:center;align-items:center;gap:20px}
.band svg{width:40px;height:40px}
.q{position:absolute;left:90px;right:90px;top:1460px;text-align:center;font-family:'Bricolage';font-weight:800;font-size:58px;line-height:1.05;letter-spacing:-1px}
.h{position:absolute;left:0;right:0;top:1610px;text-align:center;font-size:30px;font-weight:600;color:#9A8F84}
</style></head><body>
<div class="card"><img src="file://${card}"></div>
<div class="band">NOVO POST <svg viewBox="0 0 20 20"><path d="M5 3l12 7-12 7z" fill="#fff"/></svg> DESLIZA NO NOSSO PERFIL</div>
<div class="q">${pergunta}</div>
<div class="h">@tocaajantar</div>
</body></html>`;
  const tmp = path.join(dir, 'story.html');
  fs.writeFileSync(tmp, html);
  const p2 = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p2.goto('file://' + tmp);
  await p2.evaluate(() => document.fonts.ready);
  await p2.screenshot({ path: path.join(dir, 'story.jpg'), type: 'jpeg', quality: 92 });
  await browser.close();
  console.log('story.jpg');
})();

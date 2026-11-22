// Preços reais do dia no Continente Online (página pública de pesquisa).
// Uso: node tools/precos.js "peito de frango" "cebola" "tomate pelado lata"
// Mostra, para cada termo, os primeiros produtos com preço, preço por unidade (€/kg, €/l…) e o link.
// Usa um browser normal e carrega só as páginas de pesquisa (uma por termo, com pausa entre elas).
const { chromium } = require('playwright');
(async () => {
  const termos = process.argv.slice(2);
  if (!termos.length) { console.error('Indica pelo menos um ingrediente.'); process.exit(1); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ locale: 'pt-PT' });
  const hoje = new Date().toISOString().slice(0, 10);
  const out = [];
  for (const t of termos) {
    const url = 'https://www.continente.pt/pesquisa/?q=' + encodeURIComponent(t);
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForSelector('.product-tile, .productTile, [data-pid]', { timeout: 15000 }).catch(() => {});
      await page.waitForTimeout(1500);
      const itens = await page.evaluate(() => {
        const tiles = [...document.querySelectorAll('.product-tile, .productTile, div[data-pid]')].slice(0, 12);
        const seen = new Set();
        return tiles.map(el => {
          const txt = el.innerText.replace(/\s+/g, ' ').trim();
          const a = el.querySelector('a[href*="/produto/"]');
          return { txt, href: a ? a.href : '' };
        }).filter(x => x.href && !seen.has(x.href) && seen.add(x.href)).slice(0, 4);
      });
      out.push({ termo: t, url, itens });
    } catch (e) {
      out.push({ termo: t, url, erro: String(e).slice(0, 120) });
    }
    await page.waitForTimeout(1500);
  }
  await browser.close();
  console.log(`Preços Continente Online · ${hoje}`);
  for (const r of out) {
    console.log(`\n## ${r.termo}  (${r.url})`);
    if (r.erro) { console.log('  ERRO: ' + r.erro); continue; }
    if (!r.itens.length) console.log('  (sem resultados legíveis — confirma à mão)');
    for (const i of r.itens) console.log(`  - ${i.txt.slice(0, 220)}\n    ${i.href}`);
  }
})();

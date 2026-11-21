"""Gera carousel.html (7 slides, moldura 420x525). Modelo base: muda só NOME, HANDLE, FOTOS e o conteúdo dos slides."""
from pathlib import Path

HERE = Path(__file__).parent
FONTS = "../../assets/fonts"
NOME = "toca a jantar"   # wordmark do cabeçalho
HANDLE = "@tocaajantar"
# Fotografias reais (prioridade). Se o ficheiro não existir, usa a ilustração PAN.
FOTO_CAPA = HERE / "fotos" / "capa.jpg"            # prato acabado, visto de cima
FOTO_INGREDIENTES = HERE / "fotos" / "ingredientes.jpg"  # flat-lay dos ingredientes

LOGO = """<svg viewBox="0 0 40 40" class="logo"><circle cx="20" cy="22" r="15" fill="none" stroke="#2B2118" stroke-width="3.2"/>
<path d="M20 7 A15 15 0 0 1 32.99 29.5" fill="none" stroke="#E4572E" stroke-width="5" stroke-linecap="round"/>
<rect x="16" y="1.5" width="8" height="4" rx="1.5" fill="#2B2118"/><line x1="20" y1="22" x2="20" y2="13" stroke="#2B2118" stroke-width="3" stroke-linecap="round"/>
<circle cx="20" cy="22" r="2.4" fill="#2B2118"/></svg>"""

PAN = """<svg viewBox="0 0 300 220" class="pan">
<rect x="208" y="98" width="96" height="22" rx="11" fill="#2B2118" transform="rotate(-18 208 109)"/>
<circle cx="125" cy="112" r="102" fill="#2B2118"/><circle cx="125" cy="112" r="90" fill="#F6E3C6"/>
<g fill="#3A7D44">
<path d="M70 70 q22 -26 40 4 q-20 14 -40 -4z"/><path d="M150 60 q30 -12 34 20 q-24 6 -34 -20z"/>
<path d="M60 140 q10 -30 38 -12 q-14 22 -38 12z"/><path d="M160 150 q26 -22 40 8 q-24 14 -40 -8z"/>
<path d="M112 168 q18 -20 34 4 q-18 12 -34 -4z"/></g>
<g fill="#E9A23B" stroke="#C9781E" stroke-width="2">
<rect x="95" y="88" width="30" height="24" rx="7" transform="rotate(-12 110 100)"/>
<rect x="138" y="102" width="30" height="24" rx="7" transform="rotate(14 153 114)"/>
<rect x="88" y="124" width="28" height="22" rx="7" transform="rotate(8 102 135)"/>
<rect x="128" y="72" width="26" height="22" rx="7" transform="rotate(-24 141 83)"/>
<rect x="170" y="80" width="26" height="22" rx="7" transform="rotate(20 183 91)"/></g>
<g fill="#F2C879" stroke="#D9A44E" stroke-width="1.5">
<circle cx="80" cy="105" r="8"/><circle cx="126" cy="138" r="8"/><circle cx="182" cy="128" r="8"/><circle cx="150" cy="88" r="7.5"/>
<circle cx="66" cy="120" r="7.5"/><circle cx="196" cy="108" r="7.5"/><circle cx="110" cy="70" r="7.5"/><circle cx="140" cy="160" r="7.5"/>
<circle cx="170" cy="168" r="7"/><circle cx="92" cy="155" r="7"/></g>
<g fill="#FFF8EE" opacity=".9"><ellipse cx="75" cy="88" rx="7" ry="4"/><ellipse cx="170" cy="140" rx="6" ry="3.5"/></g>
<g fill="#F2E86D"><path d="M190 152 a14 14 0 0 1 22 -10 l-11 12z"/></g>
</svg>"""

DOWN = """<svg viewBox="0 0 24 24" class="down"><path d="M12 4v14M6 12l6 6 6-6" fill="none" stroke="#E4572E" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

PIN = """<svg viewBox="0 0 24 24" class="pin"><path d="M15 3l6 6-3 1-4 4 .5 4.5L13 20l-4-4-5 5-1-1 5-5-4-4 1.5-1.5L10 10l4-4z" fill="#E4572E"/></svg>"""

def frame(n, body, teaser=None, cls=""):
    foot_right = f'<span class="teaser">{teaser}</span>' if teaser else ""
    return f"""<section class="slide {cls}" id="s{n}">
  <header><div class="brand">{LOGO}<span>{NOME}</span></div><span class="count">{n}/7</span></header>
  <div class="body">{body}</div>
  <footer><span class="handle">{HANDLE}</span>{foot_right}</footer>
</section>"""

def step(num, text, mins):
    return f'<div class="step"><div class="num">{num}</div><p>{text}</p><div class="min">{mins}</div></div>'

slides = []
slides.append(frame(1, f"""
  <div class="kicker">JANTAR NUMA FRIGIDEIRA</div>
  <h1>Frango com grão e espinafres</h1>
  {('<img class="hero" src="fotos/capa.jpg" alt="">' if FOTO_CAPA.exists() else PAN)}
  <div class="chips"><span class="chip red">20 min</span><span class="chip">1 frigideira</span><span class="chip">2 pessoas</span></div>
""", "desliza →", "s1"))

slides.append(frame(2, f"""
  <h2 class="big">São 19h30.<br>Não há nada feito.</h2>
  <p class="lead">Tens uma lata de grão e um saco de espinafres? Então tens jantar.</p>
  <ul class="ticks"><li>Sem forno</li><li>Sem tachos extra para lavar</li><li>Sem pensar muito</li></ul>
  <div class="promise">{LOGO}<div><b>20 minutos</b><span>do frigorífico à mesa, numa só frigideira</span></div></div>
""", "Do que precisas →", "s2"))

ING = [("Peito de frango", "300 g"), ("Grão-de-bico cozido", "1 lata (400 g)"), ("Espinafres baby", "100 g"),
       ("Natas culinárias", "100 ml"), ("Alho", "2 dentes"), ("Azeite", "1 c. sopa"),
       ("Pimentão-doce", "1 c. chá"), ("Limão", "½"), ("Sal e pimenta", "a gosto")]
rows = "".join(f'<li><span>{a}</span><i></i><b>{b}</b></li>' for a, b in ING)
slides.append(frame(3, f"""
  <div class="kicker">INGREDIENTES · 2 PESSOAS</div>
  <h2>Cabe tudo num saco de supermercado</h2>
  {('<img class="flat" src="fotos/ingredientes.jpg" alt="">' if FOTO_INGREDIENTES.exists() else '')}
  <ul class="ing{' compact' if FOTO_INGREDIENTES.exists() else ''}">{rows}</ul>
""", "Agora, o relógio →"))

slides.append(frame(4, f"""
  
  <div class="kicker">PASSOS 1 A 3</div>
  <h2>Primeiro, o frango</h2>
  <div class="steps">
  {step(1, "Corta o frango em cubos de 2 cm. Tempera com sal, pimenta e pimentão-doce.", "3 min")}
  {step(2, "Azeite em lume médio-alto. Aloura o frango, mexendo de vez em quando, até ficar dourado por fora.", "7 min")}
  {step(3, "Junta o alho às lâminas. Mexe 1 minuto, sem deixar queimar.", "1 min")}
  </div>
  <div class="tip"><b>Truque:</b> não amontoes o frango. Em camada única aloura; amontoado, coze no próprio vapor.</div>
""", "Falta pouco →"))

slides.append(frame(5, f"""
  <div class="kicker">PASSOS 4 A 6</div>
  <h2>Depois, tudo junto</h2>
  <div class="steps">
  {step(4, "Junta o grão escorrido e as natas. Deixa borbulhar até engrossar.", "3 min")}
  {step(5, "Espinafres por cima, aos punhados. Mexe até murcharem.", "2 min")}
  {step(6, "Sumo de ½ limão, prova o sal e serve.", "1 min")}
  </div>
  <div class="safe"><b>Ponto seguro:</b> o frango está pronto com 74 °C no centro. Sem termómetro? Corta o cubo maior: não pode ter rosa.</div>
""", "Guarda o próximo →"))

slides.append(frame(6, f"""
  <div class="kicker">{PIN} GUARDA ISTO</div>
  <h2>Não tens tudo? Troca.</h2>
  <ul class="swap">
   <li><b>Sem natas</b><span>4 c. sopa de iogurte grego, já fora do lume</span></li>
   <li><b>Sem frango</b><span>camarão descascado: só 3 min no passo 2</span></li>
   <li><b>Sem espinafres</b><span>couve às tiras finas, mais 2 min</span></li>
   <li><b>Para acompanhar</b><span>arroz, pão torrado ou nada</span></li>
   <li><b>Sobras</b><span>frigorífico em menos de 2 h; come em 2 dias</span></li>
  </ul>
""", "Ajuda-nos a escolher →"))

slides.append(frame(7, f"""
  <h2 class="big">Qual é a próxima versão?</h2>
  <div class="vote"><div class="btn a"><b>A</b>Versão air fryer</div><div class="btn b"><b>B</b>Versão marmita</div></div>
  <p class="cta">Comenta <b>A</b> ou <b>B</b> {DOWN}</p>
  <p class="follow">Segue <b>{HANDLE}</b>: um jantar rápido por dia.</p>
  <p class="saveline">Guarda para a próxima vez que chegares tarde.</p>
  <p class="legal">Tempos aproximados · Confirma alergénios (contém leite)</p>
""", None, "s7"))

CSS = f"""
@font-face{{font-family:'Bricolage';src:url('{FONTS}/Bricolage.woff2') format('woff2');font-weight:200 800}}
@font-face{{font-family:'Inter';src:url('{FONTS}/Inter.woff2') format('woff2');font-weight:100 900}}
:root{{--bg:#FFF8EE;--ink:#2B2118;--red:#E4572E;--green:#3A7D44;--mustard:#F2B134;--muted:#9A8F84;--card:#FFFFFF}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#E9E2D6;font-family:'Inter',sans-serif;color:var(--ink)}}
.grid{{display:flex;flex-wrap:wrap;gap:16px;padding:16px;width:{420*4+16*5}px}}
.slide{{width:420px;height:525px;background:var(--bg);position:relative;overflow:hidden;display:flex;flex-direction:column;padding:22px 26px 18px}}
header{{display:flex;justify-content:space-between;align-items:center}}
.brand{{display:flex;align-items:center;gap:7px;font-family:'Bricolage';font-weight:800;font-size:14px;letter-spacing:-.2px}}
.logo{{width:22px;height:22px}}
.count{{font-size:11px;color:var(--muted);font-weight:600}}
.body{{flex:1;display:flex;flex-direction:column;padding-top:18px}}
footer{{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--muted);font-weight:600}}
.teaser{{color:var(--red);font-weight:700;font-size:12.5px}}
.kicker{{font-size:10.5px;letter-spacing:1.6px;font-weight:700;color:var(--green);display:flex;align-items:center;gap:5px}}
.pin{{width:13px;height:13px}}
h1{{font-family:'Bricolage';font-weight:800;font-size:43px;line-height:.98;letter-spacing:-1.4px;margin-top:8px}}
h2{{font-family:'Bricolage';font-weight:800;font-size:29px;line-height:1.05;letter-spacing:-.8px;margin:6px 0 14px}}
h2.big{{font-size:40px;letter-spacing:-1.3px;margin-top:22px}}
.pan{{width:330px;margin:14px auto 6px;display:block}}
.hero{{width:100%;height:250px;object-fit:cover;border-radius:16px;margin:12px 0 10px;display:block}}
.flat{{width:100%;height:104px;object-fit:cover;border-radius:12px;margin:-4px 0 8px;display:block}}
.ing.compact li{{padding:3.5px 0;font-size:13.5px}}
.chips{{display:flex;gap:7px;justify-content:center;margin-top:4px}}
.chip{{border:2px solid var(--ink);border-radius:99px;padding:5px 12px;font-weight:700;font-size:13px}}
.chip.red{{background:var(--red);border-color:var(--red);color:#fff}}
.lead{{font-size:17px;line-height:1.4;margin-top:6px}}
.ticks{{list-style:none;margin-top:22px}}
.ticks li{{font-size:16px;font-weight:600;padding:9px 0;border-bottom:1.5px dashed #E3D6C2;display:flex;align-items:center;gap:10px}}
.ticks li:before{{content:'';width:18px;height:18px;border-radius:50%;background:var(--green) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5 9.5l2.6 2.6L13 6.6' stroke='white' stroke-width='2.2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E")}}
.ing{{list-style:none}}
.ing li{{display:flex;align-items:baseline;gap:6px;font-size:15px;padding:7.5px 0}}
.ing li i{{flex:1;border-bottom:1.5px dotted #CDBFA9;transform:translateY(-3px)}}
.ing li b{{font-weight:700;white-space:nowrap}}
.steps{{display:flex;flex-direction:column;gap:13px}}
.step{{display:grid;grid-template-columns:34px 1fr auto;gap:10px;align-items:center;background:var(--card);border-radius:14px;padding:15px 13px;box-shadow:0 1px 0 #EADFCD}}
.num{{width:34px;height:34px;border-radius:50%;background:var(--ink);color:#fff;font-family:'Bricolage';font-weight:800;font-size:17px;display:grid;place-items:center}}
.step p{{font-size:14.6px;line-height:1.38}}
.min{{font-size:11.5px;font-weight:700;color:var(--red);background:#FCE6DE;border-radius:99px;padding:4px 8px;white-space:nowrap}}
.safe{{margin-top:16px;font-size:13px;line-height:1.4;background:#FDF1D3;border-left:4px solid var(--mustard);padding:9px 11px;border-radius:6px}}
.swap{{list-style:none;display:flex;flex-direction:column;gap:8px}}
.swap li{{background:var(--card);border-radius:12px;padding:10px 13px;display:flex;flex-direction:column;gap:2px;box-shadow:0 1px 0 #EADFCD}}
.swap b{{font-size:13px;color:var(--red)}}
.swap span{{font-size:13.5px}}
.vote{{display:flex;gap:10px;margin-top:6px}}
.btn{{flex:1;border-radius:16px;padding:16px 12px;font-weight:700;font-size:15px;display:flex;flex-direction:column;gap:6px;color:#fff}}
.btn b{{font-family:'Bricolage';font-size:34px;line-height:1}}
.btn.a{{background:var(--red)}} .btn.b{{background:var(--green)}}
.cta{{font-size:19px;font-weight:700;margin-top:18px;text-align:center}}
.follow{{font-size:14px;text-align:center;margin-top:16px}}
.saveline{{font-size:13px;text-align:center;margin-top:6px;color:var(--green);font-weight:600}}
.s2 h2.big{{font-size:41px;margin-top:14px}}
.s2 .lead{{font-size:18px}}
.s2 .ticks{{margin-top:16px}} .s2 .ticks li{{font-size:17px;padding:10px 0}}
.promise{{margin-top:auto;margin-bottom:12px;display:flex;align-items:center;gap:12px;background:#FDF1D3;border-radius:14px;padding:12px 14px}}
.promise .logo{{width:38px;height:38px;flex:none}}
.promise b{{display:block;font-family:'Bricolage';font-size:22px;letter-spacing:-.4px}}
.promise span{{font-size:13.5px}}
#s4 .step{{padding:14px 13px}} #s4 .step p{{font-size:14.8px}}
.tip{{margin-top:auto;margin-bottom:12px;font-size:13.5px;line-height:1.4;background:#E6F0E4;border-left:4px solid var(--green);padding:10px 12px;border-radius:6px}}
.down{{width:20px;height:20px;vertical-align:-3px}}
#s7 h2.big{{font-size:44px;margin-top:26px}}
#s7 .btn{{padding:22px 14px;font-size:16.5px}}
#s7 .btn b{{font-size:44px}}
#s7 .cta{{font-size:22px;margin-top:24px}}
#s7 .follow{{font-size:15.5px;margin-top:22px}}
#s7 .saveline{{font-size:14.5px}}
.legal{{margin-top:auto;margin-bottom:10px;font-size:10px;color:var(--muted);text-align:center}}
"""

html = f"""<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>{NOME} — carrossel</title>
<style>{CSS}</style></head><body><div class="grid">{''.join(slides)}</div></body></html>"""
(HERE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", HERE / "carousel.html")

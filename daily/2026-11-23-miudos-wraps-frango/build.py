"""MODELO dos carrosséis (fundo branco desde 21/11/2026). Copia para daily/<post>/build.py e muda NOME, HANDLE, fotos e conteúdo."""
from pathlib import Path

HERE = Path(__file__).parent
FONTS = "../../assets/fonts"
NOME = "toca a jantar"   # wordmark do cabeçalho
HANDLE = "@tocaajantar"
# GANCHO do slide 2: MUDA TODOS OS DIAS (nunca repetir o da semana anterior; ver report/ganchos.txt)
GANCHO = "Lancheira de amanhã?<br>Resolvida."
# CUSTO aproximado por pessoa (conta em sources.md, preços de supermercado PT do mês)
CUSTO = "≈1,10&nbsp;€"
# REGRA N.º 1: só fotografias reais (alimentos, ingredientes, prato final e acessórios).
# Se faltar uma foto, aparece um aviso FALTA FOTO REAL e o export final recusa-se a correr.
FOTO_CAPA = HERE / "fotos" / "capa.jpg"            # prato acabado, visto de cima
FOTO_INGREDIENTES = HERE / "fotos" / "ingredientes.jpg"  # flat-lay dos ingredientes

LOGO = """<svg viewBox="0 0 40 40" class="logo"><circle cx="20" cy="22" r="15" fill="none" stroke="#2B2118" stroke-width="3.2"/>
<path d="M20 7 A15 15 0 0 1 32.99 29.5" fill="none" stroke="#E4572E" stroke-width="5" stroke-linecap="round"/>
<rect x="16" y="1.5" width="8" height="4" rx="1.5" fill="#2B2118"/><line x1="20" y1="22" x2="20" y2="13" stroke="#2B2118" stroke-width="3" stroke-linecap="round"/>
<circle cx="20" cy="22" r="2.4" fill="#2B2118"/></svg>"""


DOWN = """<svg viewBox="0 0 24 24" class="down"><path d="M12 4v14M6 12l6 6 6-6" fill="none" stroke="#E4572E" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

def MISSING(ficheiro, mostra, cls):
    return f'<div class="missing-photo {cls}"><b>FALTA FOTO REAL</b><span>fotos/{ficheiro}: {mostra}</span></div>'

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
  <div class="kicker">MARMITA DOS MIÚDOS</div>
  <h1>Wraps de frango tostados</h1>
  {('<img class="hero" src="fotos/capa.jpg" alt="">' if FOTO_CAPA.exists() else MISSING('capa.jpg', 'wrap de frango tostado', 'hero'))}
  <div class="chips"><span class="chip red">15 min</span><span class="chip">lancheira</span><span class="chip">4 doses</span><span class="chip cost">{CUSTO}/dose</span></div>
""", "desliza →", "s1"))

slides.append(frame(2, f"""
  <h2 class="big">{GANCHO}</h2>
  <p class="lead">Frango, queijo e um wrap: o almoço que volta sem sobras.</p>
  <ul class="ticks"><li>Come-se frio, à mão</li><li>Legumes escondidos lá dentro</li><li>Faz-se ao jantar, para amanhã</li></ul>
  <div class="promise">{LOGO}<div><b>15 minutos</b><span>da frigideira à lancheira, 4 doses</span></div></div>
""", "Do que precisas →", "s2"))

ING = [("Wraps de trigo", "4"), ("Peito de frango", "300 g"), ("Queijo flamengo", "4 fatias"),
       ("Alface", "4 folhas"), ("Cenoura ralada", "1"), ("Iogurte natural", "1 (125 g)"),
       ("Azeite", "1 c. sopa"), ("Pimentão-doce", "1 c. chá"), ("Sal", "1 pitada")]
rows = "".join(f'<li><span>{a}</span><i></i><b>{b}</b></li>' for a, b in ING)
slides.append(frame(3, f"""
  <div class="kicker">INGREDIENTES · 4 DOSES · {CUSTO} POR DOSE</div>
  <h2>O que eles já gostam</h2>
  {('<img class="flat" src="fotos/ingredientes.jpg" alt="">' if FOTO_INGREDIENTES.exists() else MISSING('ingredientes.jpg', 'peito de frango cru', 'flat'))}
  <ul class="ing compact">{rows}</ul>
""", "Agora, o relógio →"))

slides.append(frame(4, f"""
  
  <div class="kicker">PASSOS 1 A 3</div>
  <h2>Primeiro, o frango</h2>
  <div class="steps">
  {step(1, "Corta o frango em tiras finas. Tempera com sal e pimentão&#8209;doce.", "2&nbsp;min")}
  {step(2, "Azeite em lume médio-alto. Aloura as tiras até não haver rosa por dentro.", "5&nbsp;min")}
  {step(3, "Rala a cenoura e mistura o iogurte com uma pitada de sal.", "2&nbsp;min")}
  </div>
  <div class="tip"><b>Truque:</b> tiras finas cozinham depressa e os miúdos comem-nas sem faca.</div>
""", "Falta pouco →"))

slides.append(frame(5, f"""
  <div class="kicker">PASSOS 4 A 6</div>
  <h2>Depois, enrolar</h2>
  <div class="steps">
  {step(4, "Barra o wrap com iogurte. Põe frango, queijo, alface e cenoura. Enrola bem apertado.", "3&nbsp;min")}
  {step(5, "Tosta na frigideira 1 minuto de cada lado, até ficar com marcas.", "2&nbsp;min")}
  {step(6, "Deixa arrefecer, corta ao meio e embrulha em papel vegetal.", "1&nbsp;min")}
  </div>
  <div class="safe"><b>Ponto seguro:</b> frango a 74&nbsp;°C no centro. Até sair de casa, no frigorífico; depois, lancheira térmica com 2 placas de gelo.</div>
""", "Guarda o próximo →"))

slides.append(frame(6, f"""
  <div class="kicker">{PIN} GUARDA ISTO</div>
  <h2>Não tens tudo? Troca.</h2>
  <ul class="swap">
   <li><b>Sobrou frango do jantar?</b><span>usa-o desfiado e salta os passos 1 e 2</span></li>
   <li><b>Sem frango</b><span>atum escorrido ou ovo cozido picado</span></li>
   <li><b>Não gostam de alface</b><span>milho escorrido ou pepino às tiras</span></li>
   <li><b>Para a lancheira</b><span>fruta e água; a placa de gelo por cima do wrap</span></li>
   <li><b>Na véspera</b><span>faz ao jantar; frigorífico até de manhã, come no dia seguinte</span></li>
  </ul>
""", "Ajuda-nos a escolher →"))

slides.append(frame(7, f"""
  <h2 class="big">Qual é a próxima versão?</h2>
  <div class="vote"><div class="btn a"><b>A</b>Com fiambre</div><div class="btn b"><b>B</b>Com atum</div></div>
  <p class="cta">Comenta <b>A</b> ou <b>B</b> {DOWN}</p>
  <p class="follow">Segue <b>{HANDLE}</b>: um jantar e uma marmita por dia.</p>
  <p class="saveline">Guarda para a próxima manhã de pressa.</p>
  <p class="legal">Tempos aproximados · Confirma alergénios (contém glúten e leite)</p>
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
.hero{{width:100%;height:250px;object-fit:cover;border-radius:16px;margin:12px 0 10px;display:block}}
.flat{{width:100%;height:104px;object-fit:cover;border-radius:12px;margin:-4px 0 8px;display:block}}
.ing.compact li{{padding:3.5px 0;font-size:13.5px}}
.chips{{display:flex;gap:5px;justify-content:center;margin-top:4px}}
.chip{{border:2px solid var(--ink);border-radius:99px;padding:5px 9px;font-weight:700;font-size:12px;white-space:nowrap}}
.chip.cost{{border-color:var(--green);color:var(--green)}}
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
.s2 .ticks{{margin-top:16px}} .s2 .ticks li{{font-size:17px;padding:8px 0}}
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
.missing-photo{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-align:center;border:2.5px dashed var(--red);background:#FCE6DE;color:var(--red);border-radius:16px}}
.missing-photo b{{font-family:'Bricolage';font-size:20px;letter-spacing:.5px}}
.missing-photo span{{font-size:12px;color:var(--ink)}}
.missing-photo.hero{{height:250px;margin:12px 0 10px}}
.missing-photo.flat{{height:104px;margin:-4px 0 8px;border-radius:12px}}
.legal{{margin-top:auto;margin-bottom:10px;font-size:10px;color:var(--muted);text-align:center}}
"""

html = f"""<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>{NOME} — carrossel</title>
<style>{CSS}</style></head><body><div class="grid">{''.join(slides)}</div></body></html>"""
(HERE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", HERE / "carousel.html")

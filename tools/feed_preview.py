"""Gera feed_preview.html: o post dentro de um telemóvel + grelha do perfil + próximos dias.
Uso: python3 tools/feed_preview.py daily/<pasta> <pasta_com_s1..s7.jpg>
Simulação apenas: sem logótipo nem marca do Instagram."""
import base64, html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
post = Path(sys.argv[1]).resolve()
imgs = Path(sys.argv[2]).resolve()
NOME, HANDLE = "toca a jantar", "tocaajantar"

def b64(p):
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()

slides = [b64(imgs / f"s{i}.jpg") for i in range(1, 8)]
caption = (post / "caption.txt").read_text(encoding="utf-8").strip()
first = (post / "first_comment.txt").read_text(encoding="utf-8").strip()
plan = []
for line in (ROOT / "weekly_plan.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\| (\w{3} \d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", line)
    if m and m.group(1) != "Dia":
        plan.append([c.strip() for c in m.groups()])

def esc(t):
    t = html.escape(t)
    return re.sub(r"(#\w+|@\w+)", r'<span class="tag">\1</span>', t).replace("\n", "<br>")

import datetime as _dt
_m = re.match(r"(\d{4})-(\d{2})-(\d{2})", post.name)
_d = _dt.date(int(_m[1]), int(_m[2]), int(_m[3])) if _m else _dt.date.today()
_MES = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
_DIA = ['segunda','terça','quarta','quinta','sexta','sábado','domingo']
DIA_TXT = f"{_DIA[_d.weekday()]}, {_d.day} {_MES[_d.month-1][:3]}"
DIA_CURTO = f"{_d.day} de {_MES[_d.month-1]}"
first_line = caption.split("\n")[0]
short_cap = first_line if len(first_line) <= 70 else first_line[:70].rsplit(" ", 1)[0]
m_t = re.search(r"<h1>(.*?)</h1>", (post / "carousel.html").read_text(encoding="utf-8"))
titulo = html.unescape(m_t.group(1)) if m_t else post.name
slides_html = "".join(f'<img src="{s}" alt="Slide {i+1} de 7" draggable="false">' for i, s in enumerate(slides))
dots = "".join(f'<i class="{"on" if i == 0 else ""}"></i>' for i in range(7))
pillar_tone = {"1": "t1", "2": "t2", "3": "t3", "4": "t4", "5": "t5", "6": "t6", "7": "t7"}
# Mais recente primeiro (como no perfil): os dias seguintes por cima, este post por último.
grid = ""
for d, pil, tema, _ in reversed(plan[1:]):
    grid += f'<div class="cell soon {pillar_tone.get(pil[0], "t1")}"><b>{html.escape(d)}</b><span>{html.escape(tema)}</span></div>'
grid += f'<div class="cell now"><img src="{slides[0]}" alt=""><span class="multi"></span></div>'
rows = "".join(
    f'<li class="{"cur" if i == 0 else ""}"><span class="d">{html.escape(d)}</span><span class="p">{html.escape(p)}</span><span class="t">{html.escape(t)}</span><span class="s">{html.escape(s)}</span></li>'
    for i, (d, p, t, s) in enumerate(plan))

page = f"""<title>Toca a Jantar · pré-visualização</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: telemóvel à esquerda, grelha do perfil e plano à direita; empilha em ecrã estreito */
:root{{--bg:#F3ECE1;--paper:#FFF8EE;--ink:#2B2118;--muted:#8A7F74;--line:#E3D6C2;--red:#E4572E;--green:#3A7D44;--mustard:#F2B134;--phone:#1E1813;--screen:#FFFFFF;--screenInk:#1B1612;
--display:'Bricolage Grotesque','Inter',system-ui,sans-serif;--text:'Inter',system-ui,sans-serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1A1511;--paper:#241D17;--ink:#F3EADF;--muted:#A89C8F;--line:#3A3129;--screen:#121212;--screenInk:#F2F2F2;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1A1511;--paper:#241D17;--ink:#F3EADF;--muted:#A89C8F;--line:#3A3129;--screen:#121212;--screenInk:#F2F2F2;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--text);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 48px}}
.wrap{{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:minmax(0,390px) minmax(0,1fr);gap:40px;align-items:start}}
@media (max-width:860px){{.wrap{{grid-template-columns:minmax(0,1fr)}} .phone{{margin:0 auto}}}}
h1{{font-family:var(--display);font-weight:800;font-size:clamp(28px,4vw,40px);letter-spacing:-1px;line-height:1;text-wrap:balance}}
.eyebrow{{font-size:12px;letter-spacing:1.4px;font-weight:700;color:var(--green);text-transform:uppercase;margin-bottom:8px}}
.intro{{max-width:1080px;margin:0 auto 26px}}
.intro p{{color:var(--muted);margin-top:8px;max-width:62ch;line-height:1.5}}
.phone{{width:100%;max-width:390px;background:var(--phone);border-radius:46px;padding:12px;box-shadow:0 0 0 1px var(--line),0 30px 60px rgba(0,0,0,.25)}}
.screen{{background:var(--screen);color:var(--screenInk);border-radius:36px;overflow:hidden}}
.status{{display:flex;justify-content:space-between;padding:12px 26px 6px;font-size:13px;font-weight:600}}
.top{{display:flex;align-items:center;gap:10px;padding:8px 14px}}
.av{{width:34px;height:34px;border-radius:50%;background:#FFF8EE;flex:none;display:grid;place-items:center;border:1.5px solid var(--line)}}
.av svg{{width:22px;height:22px}}
.top b{{font-size:14px}} .top small{{display:block;font-size:11.5px;opacity:.65}}
.top .more{{margin-left:auto;font-size:20px;opacity:.7;letter-spacing:1px}}
.car{{position:relative;aspect-ratio:4/5;overflow:hidden;background:#000}}
.track{{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}}
.track::-webkit-scrollbar{{display:none}}
.track img{{width:100%;height:100%;flex:none;object-fit:cover;scroll-snap-align:start;scroll-snap-stop:always;user-select:none;-webkit-user-drag:none}}
@media (prefers-reduced-motion:reduce){{.track{{scroll-behavior:auto}}}}
.count{{position:absolute;top:12px;right:12px;background:rgba(0,0,0,.6);color:#fff;font-size:12px;font-weight:600;padding:4px 9px;border-radius:99px}}
.nav{{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border-radius:50%;border:0;background:rgba(255,255,255,.9);color:#222;font-size:16px;cursor:pointer;display:grid;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.2)}}
.nav:focus-visible{{outline:3px solid var(--mustard);outline-offset:2px}}
.nav[disabled]{{opacity:0;pointer-events:none}}
.prev{{left:10px}} .next{{right:10px}}
.actions{{display:flex;align-items:center;gap:16px;padding:10px 14px 4px;position:relative}}
.actions svg{{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linejoin:round;stroke-linecap:round}}
.actions .save{{margin-left:auto}}
.dots{{position:absolute;left:50%;transform:translateX(-50%);display:flex;gap:4px}}
.dots i{{width:6px;height:6px;border-radius:50%;background:currentColor;opacity:.25}}
.dots i.on{{background:#3897F0;opacity:1}}
.cap{{padding:4px 14px 6px;font-size:13.5px;line-height:1.45}}
.cap .full{{display:none}} .cap.open .full{{display:inline}} .cap.open .short{{display:none}}
.cap button{{background:none;border:0;color:inherit;opacity:.6;font:inherit;cursor:pointer;padding:0}}
.tag{{color:#3B82C4}}
.comment{{padding:6px 14px 4px;font-size:13.5px;line-height:1.4}}
.comment small{{display:block;opacity:.55;font-size:11.5px;margin-top:3px}}
.when{{padding:4px 14px 18px;font-size:11px;opacity:.5;text-transform:uppercase;letter-spacing:.4px}}
.side{{display:flex;flex-direction:column;gap:28px;min-width:0}}
.panel{{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:20px}}
.panel h2{{font-family:var(--display);font-weight:800;font-size:22px;letter-spacing:-.4px;margin-bottom:4px}}
.panel .sub{{color:var(--muted);font-size:13px;margin-bottom:14px}}
.prof{{display:flex;gap:14px;align-items:center;margin-bottom:14px}}
.prof .av{{width:60px;height:60px}} .prof .av svg{{width:38px;height:38px}}
.prof b{{font-family:var(--display);font-size:18px}} .prof p{{font-size:13px;line-height:1.4;color:var(--muted);margin-top:2px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;max-width:420px}}
.cell{{aspect-ratio:3/4;position:relative;overflow:hidden;border-radius:2px}}
.cell img{{width:100%;height:100%;object-fit:cover}}
.cell.soon{{display:flex;flex-direction:column;justify-content:flex-end;padding:8px;gap:3px;color:#2B2118}}
.cell.soon b{{font-size:11px;letter-spacing:.6px;text-transform:uppercase;opacity:.7}}
.cell.soon span{{font-family:var(--display);font-weight:800;font-size:clamp(10.5px,3vw,13px);line-height:1.1;overflow-wrap:anywhere;hyphens:auto}}
.cell.soon b{{font-size:10px}}
.cell.soon{{padding:6px}}
.cell.empty{{background:transparent;border:1px dashed var(--line)}}
.t1{{background:#F8D9CD}} .t2{{background:#FBE6B7}} .t3{{background:#D5E8D6}} .t4{{background:#F6D3B3}} .t5{{background:#E7DFD3}} .t6{{background:#DCE4EE}} .t7{{background:#F3D6DE}}
.multi{{position:absolute;top:6px;right:6px;width:14px;height:14px;border:2px solid #fff;border-radius:3px;box-shadow:3px -3px 0 -1px rgba(255,255,255,.8)}}
.plan{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column}}
.plan li{{display:grid;grid-template-columns:64px minmax(0,150px) minmax(0,1fr);gap:4px 12px;padding:10px 0;border-top:1px solid var(--line);font-size:14px;align-items:baseline}}
.plan li .s{{grid-column:3;font-size:12px;color:var(--muted)}}
.plan .d{{font-weight:700;font-variant-numeric:tabular-nums}}
.plan .p{{color:var(--green);font-size:12.5px;font-weight:600}}
.plan li.cur .t{{font-weight:700}} .plan li.cur .d{{color:var(--red)}}
@media (max-width:520px){{.plan li{{grid-template-columns:56px minmax(0,1fr)}} .plan .t,.plan li .s{{grid-column:2}}}}
.note{{font-size:12px;color:var(--muted);line-height:1.5}}
</style>
<div class="intro">
  <div class="eyebrow">Pré-visualização · {DIA_TXT} · 10:30</div>
  <h1>{html.escape(titulo)}</h1>
  <p>O post de hoje, tal como aparece no feed. Desliza o carrossel, abre a legenda e vê onde fica na grelha do perfil. É só uma simulação.</p>
</div>
<div class="wrap">
  <div class="phone"><div class="screen">
    <div class="status"><span>10:30</span><span>5G ▮▮▮</span></div>
    <div class="top"><div class="av">@@LOGO_SVG@@</div><div><b>{HANDLE}</b><small>Receitas rápidas</small></div><span class="more">···</span></div>
    <div class="car" id="car">
      <div class="track" id="track">{slides_html}</div>
      <span class="count" id="count">1/7</span>
      <button class="nav prev" id="prev" aria-label="Slide anterior" disabled>‹</button>
      <button class="nav next" id="next" aria-label="Slide seguinte">›</button>
    </div>
    <div class="actions">
      <svg viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>
      <svg viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-3.2-6.4L21 4l-1.2 4.4A8 8 0 0 1 20 12z"/></svg>
      <svg viewBox="0 0 24 24"><path d="M21 3L3 10l7 3 3 7z"/></svg>
      <div class="dots" id="dots">{dots}</div>
      <svg class="save" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-5-6 5z"/></svg>
    </div>
    <div class="cap" id="cap"><b>{HANDLE}</b> <span class="short">{esc(short_cap)}… <button id="more" type="button">mais</button></span><span class="full">{esc(caption)} <button id="less" type="button">menos</button></span></div>
    <div class="comment"><b>{HANDLE}</b> {esc(first)}<small>Primeiro comentário (fixado)</small></div>
    <div class="when">{DIA_CURTO}</div>
  </div></div>
  <div class="side">
    <section class="panel">
      <h2>Grelha do perfil</h2>
      <p class="sub">Corte 3:4. Assim fica o perfil no sábado, 28: o mais recente em cima à esquerda; este post é o último.</p>
      <div class="prof"><div class="av">@@LOGO_SVG@@</div><div><b>{NOME}</b><p>Jantares em 20 min com ingredientes do supermercado e pouca loiça 🍳 Uma receita nova por dia. Guarda e segue para nunca mais ficares sem ideias.</p></div></div>
      <div class="grid">{grid}</div>
    </section>
    <section class="panel">
      <h2>Próximos 7 dias</h2>
      <p class="sub">Nunca o mesmo pilar em dois dias seguidos.</p>
      <ul class="plan">{rows}</ul>
    </section>
    <p class="note">Simulação sem a marca nem o logótipo do Instagram. Os slides estão em pré-visualização a 840×1050; a exportação final é a 1080×1350.</p>
  </div>
</div>
<script>
(function(){{
  var n=7,track=document.getElementById('track'),count=document.getElementById('count'),
      prev=document.getElementById('prev'),next=document.getElementById('next'),dots=document.querySelectorAll('#dots i'),i=0;
  function paint(){{count.textContent=(i+1)+'/'+n;prev.disabled=i===0;next.disabled=i===n-1;
    dots.forEach(function(d,j){{d.className=j===i?'on':''}});}}
  function go(k){{k=Math.max(0,Math.min(n-1,k));track.scrollTo({{left:k*track.clientWidth}});}}
  track.addEventListener('scroll',function(){{var k=Math.round(track.scrollLeft/track.clientWidth);if(k!==i){{i=k;paint();}}}},{{passive:true}});
  prev.onclick=function(){{go(i-1)}};next.onclick=function(){{go(i+1)}};
  track.tabIndex=0;track.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'){{e.preventDefault();go(i+1)}}if(e.key==='ArrowLeft'){{e.preventDefault();go(i-1)}}}});
  var cap=document.getElementById('cap');
  document.getElementById('more').onclick=function(){{cap.classList.add('open')}};
  document.getElementById('less').onclick=function(){{cap.classList.remove('open')}};
  paint();
}})();
</script>
"""
LOGO = '<svg viewBox="0 0 40 40"><circle cx="20" cy="22" r="15" fill="none" stroke="#2B2118" stroke-width="3.2"/><path d="M20 7 A15 15 0 0 1 32.99 29.5" fill="none" stroke="#E4572E" stroke-width="5" stroke-linecap="round"/><rect x="16" y="1.5" width="8" height="4" rx="1.5" fill="#2B2118"/><line x1="20" y1="22" x2="20" y2="13" stroke="#2B2118" stroke-width="3" stroke-linecap="round"/><circle cx="20" cy="22" r="2.4" fill="#2B2118"/></svg>'
page = page.replace("@@LOGO_SVG@@", LOGO)
fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700..800&family=Inter:wght@400..700&display=swap">\n'
(post / "feed_preview.html").write_text(fonts + page, encoding="utf-8")
print("ok", post / "feed_preview.html")

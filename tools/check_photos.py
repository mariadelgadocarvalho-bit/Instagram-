"""Verifica as fotos de um post (Regra n.º 1: tudo real, incluindo acessórios).
Uso: python3 tools/check_photos.py daily/<pasta>

Verificações automáticas (sinais, não provas):
- largura >= 1080 px;
- JPEG com EXIF de câmara (marca/modelo/data). Um PNG sem EXIF, em baixa resolução, é sinal de IA;
- metadados de IA conhecidos (C2PA / "trainedAlgorithmicMedia", nomes de geradores);
- registo da foto em fotos/fotos.md (origem, autor, o que mostra).
As verificações manuais (mostra exatamente a receita? os acessórios são reais?) continuam obrigatórias.
"""
import sys
from pathlib import Path
from PIL import Image, ExifTags

AI_MARKERS = [b"trainedAlgorithmicMedia", b"c2pa", b"Midjourney", b"DALL", b"Stable Diffusion",
              b"Firefly", b"Imagen", b"Canva AI", b"GPT-4o", b"compositeWithTrainedAlgorithmicMedia"]

post = Path(sys.argv[1])
fotos = post / "fotos"
registo = (fotos / "fotos.md").read_text(encoding="utf-8") if (fotos / "fotos.md").exists() else ""
files = sorted(p for p in fotos.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic"})
needed = ["capa.jpg", "ingredientes.jpg"]
ok = True
for n in needed:
    if not (fotos / n).exists():
        print(f"FALTA  {n}")
        ok = False
for f in files:
    probs, notas = [], []
    im = Image.open(f)
    w, h = im.size
    if w < 1080:
        probs.append(f"largura {w}px < 1080")
    raw = f.read_bytes()
    hits = [m.decode() for m in AI_MARKERS if m.lower() in raw.lower()]
    if hits:
        probs.append("metadados de IA: " + ", ".join(hits))
    exif = {ExifTags.TAGS.get(k, k): v for k, v in (im.getexif() or {}).items()}
    cam = " ".join(str(exif.get(k, "")) for k in ("Make", "Model")).strip()
    if cam:
        notas.append(f"câmara: {cam}")
    else:
        notas.append("sem EXIF de câmara (normal em bancos de fotos; suspeito se for PNG sem autor)")
        if f.suffix.lower() == ".png":
            probs.append("PNG sem EXIF: confirmar que não é IA")
    if f.name not in registo:
        probs.append("não está registada em fotos/fotos.md")
    estado = "OK    " if not probs else "ATENÇÃO"
    if probs:
        ok = False
    print(f"{estado} {f.name} {w}x{h} · " + "; ".join(probs + notas))
print("\nResultado:", "fotos aprovadas nas verificações automáticas" if ok else "NÃO APROVADO: corrige antes de exportar")
print("Falta sempre a verificação manual: mostra exatamente a receita? Os acessórios são reais?")
sys.exit(0 if ok else 1)

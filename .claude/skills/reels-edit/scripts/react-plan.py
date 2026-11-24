#!/usr/bin/env python3
"""react-plan.py: the timeline of a React com pausa, plus the checks that keep it legal and in style.

A react alternates, in order: TRECHO (the original plays in the bottom of a split screen, you react in the top box)
-> PAUSA (the last frame of that excerpt freezes and darkens, a pause icon and a click) -> FALA (you, full screen).
Then the next excerpt picks up exactly where the last one stopped.

Input (react.json; paths relative to the file):
  {"id": "react-ela-x", "original": "public/original.mp4", "credito": "@autor",
   "titulo": "ELA ACHA QUE O PROBLEMA\\nSAO OS HOMENS?",
   "reacao": "public/reacao.mp4", "reacao_offset": 2.31,      # optional: you watching; offset = sync-tracks.py result
   "trechos": [[0, 9.5], [9.5, 21.0], [21.0, 30.2]],          # seconds of the ORIGINAL played before each pause
   "falas": ["public/fala-1.mp4", "public/fala-2.mp4", "public/fala-3.mp4"],   # one flat-cut file per pause
   "pausa": 0.5}
Writes react-plan.json and REACT-PLAN.md next to react.json and pausa-N.png (the frozen frames) into --public.

Rules (from ESTILO.md; numbers adjustable with flags):
  FAIL  credito missing; titulo missing; falas count != trechos count; a trecho outside the original or not after the
        previous one; any trecho longer than --max-trecho (12 s); your share of the film under --min-share (60 %)
  WARN  pauses outside 2-4; total outside 45-90 s; no reacao take (the top box would have nothing to show)
Exit 1 on any FAIL (the plan is still written so you can read it).

Usage: python3 react-plan.py --spec videos/<p>/react.json --public videos/<p>/public [--fps 30]
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--public", required=True)
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--max-trecho", type=float, default=12.0)
ap.add_argument("--min-share", type=float, default=0.60)
args = ap.parse_args()

base = os.path.dirname(os.path.abspath(args.spec))
spec = json.load(open(args.spec))
P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)

def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    if r.returncode or not r.stdout.strip():
        sys.exit("ffprobe could not read %s" % path)
    return float(r.stdout.strip())

fails, warns = [], []
if not str(spec.get("credito", "")).strip():
    fails.append("sem credito: o @ do autor original fica na tela o tempo todo (lei 9.610, art. 46, III)")
if not str(spec.get("titulo", "")).strip():
    fails.append("sem titulo: o quadro 0 precisa da pergunta provocativa")
orig = P(spec["original"]); d_orig = duration(orig)
trechos = [(float(a), float(b)) for a, b in spec["trechos"]]
falas = [P(f) for f in spec["falas"]]
if len(falas) != len(trechos):
    fails.append("%d trechos e %d falas: precisa de uma fala depois de cada trecho" % (len(trechos), len(falas)))
prev = 0.0
for i, (a, b) in enumerate(trechos, 1):
    if not (0 <= a < b <= d_orig + 1e-3):
        fails.append("trecho %d (%.2f-%.2f) fora do original (0-%.2f s)" % (i, a, b, d_orig))
    if a < prev - 1e-3:
        fails.append("trecho %d comeca em %.2f, antes do fim do anterior (%.2f)" % (i, a, prev))
    if b - a > args.max_trecho + 1e-6:
        fails.append("trecho %d tem %.1f s (maximo %.0f s): corte o trecho ou pause antes" % (i, b - a, args.max_trecho))
    prev = b
reacao = spec.get("reacao")
if not reacao:
    warns.append("sem gravacao de reacao: a caixa de cima do layout dividido fica vazia; grave voce assistindo ao original")
off = float(spec.get("reacao_offset", 0.0))
pausa = float(spec.get("pausa", 0.5))

os.makedirs(args.public, exist_ok=True)
segs, t = [], 0.0
for i, (a, b) in enumerate(trechos, 1):
    segs.append({"tipo": "trecho", "n": i, "start": round(t, 3), "dur": round(b - a, 3), "media_start": a,
                 "reacao_media_start": round(off + a, 3) if reacao else None}); t += b - a
    frame = "pausa-%d.png" % i
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % max(0.0, b - 1.0 / args.fps), "-i", orig, "-frames:v", "1",
                    os.path.join(args.public, frame)], check=True)
    segs.append({"tipo": "pausa", "n": i, "start": round(t, 3), "dur": pausa, "frame": frame}); t += pausa
    if i <= len(falas):
        df = duration(falas[i - 1])
        segs.append({"tipo": "fala", "n": i, "start": round(t, 3), "dur": round(df, 3),
                     "src": os.path.relpath(falas[i - 1], os.path.abspath(args.public))}); t += df
total = round(t, 3)
d_fala = sum(s["dur"] for s in segs if s["tipo"] == "fala")
share = d_fala / total if total else 0
if share < args.min_share:
    fails.append("sua fala e %.0f%% do video (minimo %.0f%%): fale mais ou encurte os trechos" % (100 * share, 100 * args.min_share))
if not 2 <= len(trechos) <= 4:
    warns.append("%d pausas (o estilo pede de 2 a 4)" % len(trechos))
if not 45 <= total <= 90:
    warns.append("duracao %.1f s (o estilo pede de 45 a 90 s)" % total)

plan = {"id": spec.get("id"), "duration": total, "fps": args.fps, "credito": spec.get("credito"), "titulo": spec.get("titulo"),
        "original": os.path.relpath(orig, os.path.abspath(args.public)),
        "reacao": os.path.relpath(P(reacao), os.path.abspath(args.public)) if reacao else None,
        "share_fala": round(share, 3), "segments": segs, "fails": fails, "warns": warns}
json.dump(plan, open(os.path.join(base, "react-plan.json"), "w"), indent=1, ensure_ascii=False)
md = ["# Plano do react: %s" % (spec.get("id") or ""), "",
      "**%s**: %.1f s, sua fala %.0f%%, %d pausas, credito %s" % ("FAIL" if fails else "OK", total, 100 * share, len(trechos), spec.get("credito")), "",
      "| # | Tipo | Inicio | Duracao | Fonte |", "|---|---|---|---|---|"]
for s in segs:
    src = ("original %.2f-%.2f s" % (s["media_start"], s["media_start"] + s["dur"])) if s["tipo"] == "trecho" else s.get("frame") or s.get("src")
    md.append("| %d | %s | %.2f | %.2f | %s |" % (s["n"], s["tipo"], s["start"], s["dur"], src))
md += [""] + ["- FAIL: " + f for f in fails] + ["- WARN: " + w for w in warns]
open(os.path.join(base, "REACT-PLAN.md"), "w").write("\n".join(md) + "\n")
for f in fails: print("FAIL", f)
for w in warns: print("WARN", w)
print("%s: %.1f s, fala %.0f%%, %d segmentos -> %s" % ("FAIL" if fails else "OK", total, 100 * share, len(segs), os.path.join(base, "react-plan.json")))
sys.exit(1 if fails else 0)

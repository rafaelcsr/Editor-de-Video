#!/usr/bin/env python3
"""react-compose.py: react-plan.json -> public/index.html, the React com pausa layout from ESTILO.md (format 4.0).

Builds the skeleton only; captions of your speech are added afterwards by hand, following the HyperFrames captions
skill and ESTILO.md 3.4 (legenda de destaque). Layout, 1080x1920:
  TRECHO   top box y 0-640: you watching (reacao, muted, synced), yellow #FCCD02 12 px frame drawn as its own overlay;
           bottom y 640-1920: the original (cover crop, --orig-pos); credit pill on the seam (y 614-666);
           the opening title in the top box at y 236 (2 lines, 56 px, inside x 60-940)
  PAUSA    the excerpt's last frame frozen over the bottom, darkened 35 %, a white pause icon, a click (if click.mp3 is there)
  FALA     you, full screen; nothing else (captions go here)
Every <video> is top level: HyperFrames resolves a video's start from its own data-start, so nesting it inside a timed
<div> shows the wrong frames (check: video_nested_in_timed_element).
Copies gsap.min.js, the Montserrat files and click.mp3 (media-use library) into public/ when found.

Usage: python3 react-compose.py --plan videos/<p>/react-plan.json --public videos/<p>/public [--orig-pos "50% 30%"] [--react-pos "50% 40%"]
"""
import argparse, html, json, os, shutil

ap = argparse.ArgumentParser()
ap.add_argument("--plan", required=True)
ap.add_argument("--public", required=True)
ap.add_argument("--orig-pos", default="50% 30%", help="object-position of the original inside the bottom box")
ap.add_argument("--react-pos", default="50% 40%", help="object-position of your reaction take inside the top box")
args = ap.parse_args()

SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = json.load(open(args.plan))
pub = args.public; os.makedirs(os.path.join(pub, "fonts"), exist_ok=True)
for src, dst in ((os.path.join(SK, "assets", "vendor", "gsap.min.js"), "gsap.min.js"),
                 (os.path.join(SK, "assets", "fonts", "montserrat-latin-800-normal.woff2"), "fonts/montserrat-latin-800-normal.woff2"),
                 (os.path.join(SK, "assets", "fonts", "montserrat-latin-900-italic.woff2"), "fonts/montserrat-latin-900-italic.woff2")):
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(pub, dst))
click = None
for c in (os.path.join(pub, "click.mp3"), os.path.join(SK, "assets", "sfx", "clique", "clique-mouse.mp3"), os.path.join(SK, "..", "media-use", "audio", "assets", "sfx", "click.mp3"),
          os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx/click.mp3")):
    if os.path.exists(c):
        if os.path.abspath(c) != os.path.abspath(os.path.join(pub, "click.mp3")):
            shutil.copyfile(c, os.path.join(pub, "click.mp3"))
        click = "click.mp3"; break

D = p["duration"]; segs = p["segments"]; esc = html.escape
titulo = "<br>".join(esc(x) for x in str(p["titulo"]).split("\n"))
cred = esc(str(p["credito"])) + " · vídeo original"
el = []
for s in segs:
    n, st = s["n"], s["start"]
    if s["tipo"] == "trecho":
        pz = next(x for x in segs if x["tipo"] == "pausa" and x["n"] == n)
        d = round(s["dur"] + pz["dur"], 3)
        cheia = s.get("layout") == "cheia"
        if cheia:   # the original alone, full screen: no top box, credit low on the frame, no title
            el.append('<video class="origcheia" id="ori%d" src="%s" playsinline data-has-audio="true" data-start="%s" data-duration="%s" data-media-start="%s" data-track-index="4"></video>'
                      % (n, esc(p["original"]), st, s["dur"], s["media_start"]))
            el.append('<div class="clip selo selobaixo" id="selo%d" data-start="%s" data-duration="%s" data-track-index="7">%s</div>' % (n, st, d, cred))
            continue
        if p.get("reacao"):
            el.append('<video class="rea" id="rea%d" src="%s" muted playsinline data-start="%s" data-duration="%s" data-media-start="%s" data-track-index="3"></video>'
                      % (n, esc(p["reacao"]), st, d, s["reacao_media_start"]))
        el.append('<video class="orig" id="ori%d" src="%s" playsinline data-has-audio="true" data-start="%s" data-duration="%s" data-media-start="%s" data-track-index="4"></video>'
                  % (n, esc(p["original"]), st, s["dur"], s["media_start"]))
        el.append('<div class="clip moldura" id="mold%d" data-start="%s" data-duration="%s" data-track-index="6"></div>' % (n, st, d))
        el.append('<div class="clip selo" id="selo%d" data-start="%s" data-duration="%s" data-track-index="7">%s</div>' % (n, st, d, cred))
        el.append('<div class="clip titulo" id="tit%d" data-start="%s" data-duration="%s" data-track-index="8">%s</div>' % (n, st, d, titulo))
    elif s["tipo"] == "pausa":
        if next(x for x in segs if x["tipo"] == "trecho" and x["n"] == n).get("layout") == "cheia":
            el.append('<img class="clip congelado congcheio" id="cong%d" src="%s" data-start="%s" data-duration="%s" data-track-index="5">' % (n, esc(s["frame"]), st, s["dur"]))
            el.append('<div class="clip escuro escurocheio" id="esc%d" data-start="%s" data-duration="%s" data-track-index="9"><i></i><i></i></div>' % (n, st, s["dur"]))
            if click:
                el.append('<audio id="clk%d" src="%s" data-start="%s" data-duration="0.3" data-track-index="10" data-volume="0.28"></audio>' % (n, click, st))
            continue
        el.append('<img class="clip congelado" id="cong%d" src="%s" data-start="%s" data-duration="%s" data-track-index="5">' % (n, esc(s["frame"]), st, s["dur"]))
        el.append('<div class="clip escuro" id="esc%d" data-start="%s" data-duration="%s" data-track-index="9"><i></i><i></i></div>' % (n, st, s["dur"]))
        if click:
            el.append('<audio id="clk%d" src="%s" data-start="%s" data-duration="0.3" data-track-index="10" data-volume="0.28"></audio>' % (n, click, st))
    else:   # fala or gancho: you, full screen
        el.append('<video class="fala" id="fala%d" src="%s" playsinline data-has-audio="true" data-start="%s" data-duration="%s" data-track-index="1"></video>'
                  % (n, esc(s["src"]), st, s["dur"]))

doc = """<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="gsap.min.js"></script>
<style>
@font-face{font-family:M;src:url(fonts/montserrat-latin-800-normal.woff2) format("woff2");font-weight:800}
@font-face{font-family:MI;src:url(fonts/montserrat-latin-900-italic.woff2) format("woff2");font-weight:900;font-style:italic}
:root{--branco:#FFFFFF;--amarelo:#FCCD02;--painel:#21272D}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
#stage{position:relative;width:1080px;height:1920px;font-family:M}
.rea{position:absolute;left:0;top:0;width:1080px;height:640px;object-fit:cover;object-position:%(rpos)s}
.orig{position:absolute;left:0;top:640px;width:1080px;height:1280px;object-fit:cover;object-position:%(opos)s}
.congelado{position:absolute;left:0;top:640px;width:1080px;height:1280px;object-fit:cover;object-position:%(opos)s;z-index:4}
.escuro{position:absolute;left:0;top:640px;width:1080px;height:1280px;background:rgba(0,0,0,.35);z-index:5;display:flex;align-items:center;justify-content:center;gap:28px}
.escuro i{display:block;width:28px;height:110px;background:var(--branco);border-radius:6px}
.moldura{position:absolute;left:0;top:0;width:1080px;height:640px;box-shadow:inset 0 0 0 12px var(--amarelo);z-index:6}
.selo{position:absolute;left:50%%;top:614px;transform:translateX(-50%%);height:52px;padding:0 26px;border-radius:26px;background:var(--amarelo);color:var(--painel);font:800 30px/52px M;white-space:nowrap;z-index:7}
.titulo{position:absolute;left:60px;width:880px;top:236px;text-align:center;color:var(--branco);font:800 56px/1.15 M;text-transform:uppercase;text-shadow:0 2px 12px rgba(0,0,0,.6);z-index:7}
.fala{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.origcheia{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;object-position:%(opos)s}
.selobaixo{top:1380px}
.congcheio{top:0;height:1920px}
.escurocheio{top:0;height:1920px}
/* legenda limpa com destaque pontual (ESTILO 3.4 / DIRECAO 11): <div class="clip leg" ...>Isso é <b>postura</b>.</div>
   a legenda do original (quando ele nao tiver): <div class="clip leg legorig" ...> */
.leg{position:absolute;left:60px;width:880px;top:1310px;text-align:center;color:var(--branco);font:800 58px/1.15 M;text-shadow:0 2px 10px rgba(0,0,0,.75),0 0 2px rgba(0,0,0,.9);z-index:8}
.leg b{color:var(--amarelo);font-weight:800}
.legorig{top:1180px;font-size:46px;color:rgba(255,255,255,.9)}
</style></head><body>
<div id="stage" data-composition-id="%(id)s" data-start="0" data-duration="%(D)s" data-fps="30" data-width="1080" data-height="1920">
%(el)s
<!-- legendas da sua fala aqui -->
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
tl.set({}, {}, %(D)s);
window.__timelines["%(id)s"] = tl;
</script>
</body></html>
""" % {"rpos": args.react_pos, "opos": args.orig_pos, "id": esc(str(p.get("id") or "react")), "D": D, "el": "\n".join(el)}
out = os.path.join(pub, "index.html")
open(out, "w").write(doc)
print("wrote %s: %.1f s, %d elements%s" % (out, D, len(el), "" if click else " (no click.mp3 found: pauses are silent)"))

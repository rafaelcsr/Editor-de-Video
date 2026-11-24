#!/usr/bin/env python3
"""formato.py: decide the output format of a video (vertical Reels or horizontal 16:9) and print the flags to use.

  vertical (default)  1080x1920, 30 fps, safe area x 60-940 / y 220-1500 (Instagram)
  horizontal          1920x1080, the recording's frame rate rounded (24, 25, 30, 50, 60; capped at 60), text 5% from the
                      edges and above the player controls: x 96-1824 / y 54-950
Horizontal when --modo horizontal (the user said "horizontal", "YouTube" or "16:9"), or with --modo auto (default) when the
recording itself is wider than tall. BT.709 in both.

Usage: python3 formato.py --video raw/clip.mp4 [--modo auto|vertical|horizontal] [--json]
"""
import argparse, json, subprocess, sys
from fractions import Fraction

ap = argparse.ArgumentParser()
ap.add_argument("--video")
ap.add_argument("--modo", default="auto", choices=["auto", "vertical", "horizontal"])
ap.add_argument("--json", action="store_true")
a = ap.parse_args()

w = h = None; rate = Fraction(30)
if a.video:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:stream_side_data=rotation",
                        "-of", "json", a.video], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffprobe could not read %s" % a.video)
    st = json.loads(r.stdout)["streams"][0]
    w, h = int(st["width"]), int(st["height"])
    rot = next((abs(int(sd.get("rotation", 0))) for sd in st.get("side_data_list", []) if "rotation" in sd), 0)
    if rot in (90, 270):          # phones store vertical video as landscape + rotation
        w, h = h, w
    rate = Fraction(st.get("r_frame_rate", "30/1")) or Fraction(30)
modo = a.modo
if modo == "auto":
    modo = "horizontal" if (w and h and w > h) else "vertical"
if modo == "horizontal":
    fps = min(60, int(round(float(rate))))
    fps = min((24, 25, 30, 50, 60), key=lambda x: abs(x - fps))
    out = {"modo": "horizontal", "size": "1920x1080", "fps": fps, "resolution": "landscape",
           "safe": {"x0": 96, "x1": 1824, "y0": 54, "y1": 950}}
else:
    out = {"modo": "vertical", "size": "1080x1920", "fps": 30, "resolution": "portrait",
           "safe": {"x0": 60, "x1": 940, "y0": 220, "y1": 1500}}
out["source"] = {"width": w, "height": h, "fps": round(float(rate), 3)} if w else None
if a.json:
    print(json.dumps(out))
else:
    print("modo %s: %s a %d fps | apply-cut --size %s --fps %d | render --resolution %s --fps %d | verify-render --res %s --fps %d | safe-area --modo %s"
          % (out["modo"], out["size"], out["fps"], out["size"], out["fps"], out["resolution"], out["fps"], out["size"], out["fps"], out["modo"]))

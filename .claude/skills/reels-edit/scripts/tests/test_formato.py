"""formato.py picks vertical by default and horizontal for 16:9 recordings, keeping their frame rate up to 60;
safe-area.mjs and broll-conform.py follow the horizontal canvas."""
import json, os, shutil, subprocess, unittest
from .helpers import SCRIPTS, ffmpeg, needs_ffmpeg, run, scratch, write

NODE = shutil.which("node")
CHROME = os.path.exists("/usr/bin/google-chrome") or os.path.exists("/opt/pw-browsers/chromium")


def clip(d, name, size, rate):
    p = os.path.join(d, name)
    ffmpeg("-f", "lavfi", "-i", "testsrc2=size=%s:rate=%s:duration=1" % (size, rate), "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", p)
    return p


@needs_ffmpeg
class Formato(unittest.TestCase):
    def fmt(self, *args):
        r = run("formato.py", "--json", *args)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_default_is_vertical(self):
        d = scratch(self)
        f = self.fmt("--video", clip(d, "v.mp4", "216x384", "30"))
        self.assertEqual((f["modo"], f["size"], f["fps"]), ("vertical", "1080x1920", 30))
        self.assertEqual(self.fmt()["modo"], "vertical")

    def test_wide_recording_goes_horizontal_and_keeps_its_rate(self):
        d = scratch(self)
        f = self.fmt("--video", clip(d, "h.mp4", "384x216", "60000/1001"))
        self.assertEqual((f["modo"], f["size"], f["fps"], f["safe"]["y1"]), ("horizontal", "1920x1080", 60, 950))
        f = self.fmt("--video", clip(d, "h24.mp4", "384x216", "24"))
        self.assertEqual(f["fps"], 24)

    def test_rate_is_capped_at_60_and_user_can_force(self):
        d = scratch(self)
        self.assertEqual(self.fmt("--video", clip(d, "h120.mp4", "384x216", "120"))["fps"], 60)
        f = self.fmt("--video", clip(d, "v2.mp4", "216x384", "30"), "--modo", "horizontal")
        self.assertEqual((f["modo"], f["fps"]), ("horizontal", 30))

    def test_broll_conform_horizontal(self):
        d = scratch(self)
        out = os.path.join(d, "b.mp4")
        r = run("broll-conform.py", "--in", clip(d, "s.mp4", "640x360", "24"), "--out", out, "--size", "1920x1080", "--fps", "60")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("1920x1080, 60/1 fps", r.stdout)


@unittest.skipUnless(NODE and CHROME, "needs node and Chrome")
class SafeAreaHorizontal(unittest.TestCase):
    def go(self, body):
        d = scratch(self)
        idx = write(os.path.join(d, "index.html"), '<!doctype html><html><body style="margin:0;width:1920px;height:1080px;position:relative">'
                    '<div id="s" data-composition-id="t" data-start="0" data-duration="1" data-width="1920" data-height="1080">%s</div></body></html>' % body)
        return subprocess.run([NODE, os.path.join(SCRIPTS, "safe-area.mjs"), "--index", idx, "--modo", "horizontal", "--at", "0"], capture_output=True, text=True)

    def test_inside_passes(self):
        r = self.go('<p style="position:absolute;left:200px;top:800px;font:60px sans-serif">Legenda dentro</p>')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_over_the_player_controls_fails(self):
        r = self.go('<p style="position:absolute;left:200px;top:990px;font:60px sans-serif">Em cima dos controles</p>')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("base", r.stdout)

    def test_too_close_to_the_edge_fails(self):
        r = self.go('<p style="position:absolute;left:40px;top:300px;font:60px sans-serif">Borda</p>')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

"""safe-area.mjs: text inside x 60-940, y 220-1500 passes; text that leaves the area, or a wrong canvas size, fails."""
import os, shutil, unittest
from .helpers import SCRIPTS, scratch, write, run as _run
import subprocess

NODE = shutil.which("node")
CHROME = os.path.exists("/usr/bin/google-chrome") or os.path.exists("/opt/pw-browsers/chromium")


def page(body, w=1080, h=1920):
    return ('<!doctype html><html><body style="margin:0;width:1080px;height:1920px;position:relative">'
            '<div id="stage" data-composition-id="t" data-start="0" data-duration="2" data-width="%d" data-height="%d">%s</div></body></html>' % (w, h, body))


@unittest.skipUnless(NODE and CHROME, "needs node and Chrome")
class SafeArea(unittest.TestCase):
    def go(self, html, *extra):
        d = scratch(self)
        idx = write(os.path.join(d, "index.html"), html)
        return subprocess.run([NODE, os.path.join(SCRIPTS, "safe-area.mjs"), "--index", idx, "--at", "0,1", *extra], capture_output=True, text=True)

    def test_inside_passes(self):
        r = self.go(page('<p style="position:absolute;left:100px;top:600px;width:800px;font:60px sans-serif">Dentro da área</p>'))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS", r.stdout)

    def test_caption_too_low_fails(self):
        r = self.go(page('<p style="position:absolute;left:100px;top:1550px;width:800px;font:60px sans-serif">Legenda baixa demais</p>'))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("base", r.stdout)

    def test_title_too_wide_fails(self):
        r = self.go(page('<p style="position:absolute;left:20px;top:400px;white-space:nowrap;font:60px sans-serif">Título que encosta na borda esquerda</p>'))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("esquerda", r.stdout)

    def test_hidden_or_ignored_text_is_skipped(self):
        r = self.go(page('<p style="position:absolute;left:0;top:50px;opacity:0;font:60px sans-serif">invisível</p>'
                         '<p data-safe-ignore style="position:absolute;left:0;top:1800px;font:60px sans-serif">marca</p>'))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_text_outside_its_clip_window_is_skipped(self):
        r = self.go(page('<p class="clip" data-start="5" data-duration="2" style="position:absolute;left:0;top:50px;font:60px sans-serif">depois</p>'))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_wrong_canvas_fails(self):
        r = self.go(page("", 1920, 1080))
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()

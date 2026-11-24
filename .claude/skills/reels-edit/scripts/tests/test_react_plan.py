"""react-plan.py: the timeline alternates trecho -> pausa -> fala, and the legal/style rules fail when broken."""
import os, unittest
from .helpers import ffmpeg, load, needs_ffmpeg, read, run, scratch, write


def clip(path, dur, size="216x384"):
    ffmpeg("-f", "lavfi", "-i", "testsrc2=size=%s:rate=30:duration=%s" % (size, dur), "-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=%s" % dur,
           "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", path)
    return path


@needs_ffmpeg
class ReactPlan(unittest.TestCase):
    def setup(self, trechos, falas_dur, credito="@autor", reacao=True):
        d = scratch(self); pub = os.path.join(d, "public"); os.makedirs(pub)
        clip(os.path.join(pub, "original.mp4"), 40)
        falas = []
        for i, fd in enumerate(falas_dur, 1):
            falas.append("public/" + os.path.basename(clip(os.path.join(pub, "fala-%d.mp4" % i), fd)))
        spec = {"id": "t", "original": "public/original.mp4", "credito": credito, "titulo": "ELA ESTA CERTA?",
                "trechos": trechos, "falas": falas, "pausa": 0.5}
        if reacao:
            clip(os.path.join(pub, "reacao.mp4"), 45); spec.update(reacao="public/reacao.mp4", reacao_offset=1.5)
        return d, pub, write(os.path.join(d, "react.json"), spec)

    def test_good_plan(self):
        d, pub, spec = self.setup([[0, 8], [8, 17], [17, 26]], [12, 14, 16])
        r = run("react-plan.py", "--spec", spec, "--public", pub)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        p = load(os.path.join(d, "react-plan.json"))
        self.assertEqual([s["tipo"] for s in p["segments"]], ["trecho", "pausa", "fala"] * 3)
        self.assertAlmostEqual(p["duration"], 26 + 1.5 + 42, delta=0.2)
        t2 = p["segments"][3]
        self.assertEqual((t2["media_start"], t2["reacao_media_start"]), (8.0, 9.5))   # picks up where it stopped; reaction synced
        self.assertAlmostEqual(t2["start"], 8 + 0.5 + 12, delta=0.1)
        self.assertTrue(os.path.exists(os.path.join(pub, "pausa-3.png")))
        self.assertIn("| 1 | trecho |", read(os.path.join(d, "REACT-PLAN.md")))

    def test_compose_builds_top_level_videos(self):
        d, pub, spec = self.setup([[0, 8], [8, 17], [17, 26]], [12, 14, 16])
        self.assertEqual(run("react-plan.py", "--spec", spec, "--public", pub).returncode, 0)
        r = run("react-compose.py", "--plan", os.path.join(d, "react-plan.json"), "--public", pub)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        html = read(os.path.join(pub, "index.html"))
        self.assertEqual(html.count("<video"), 3 + 3 + 3)               # reacao + original per trecho, plus 3 falas
        self.assertIn('data-media-start="8.0"', html)
        self.assertIn('data-width="1080" data-height="1920"', html)
        self.assertIn("@autor · vídeo original", html)
        self.assertNotRegex(html, r'<div(?![^>]*data-composition-id)[^>]*data-start[^>]*>\s*<video')   # never a video inside a timed div
        self.assertTrue(os.path.exists(os.path.join(pub, "gsap.min.js")))

    def test_hook_full_original_and_integral(self):
        d, pub, spec = self.setup([[0, 8], {"de": 8, "ate": 22, "layout": "cheia", "integral": True, "motivo": "ouvir inteira"}], [14, 20])
        import json
        sp = json.load(open(spec)); sp["gancho"] = "public/fala-1.mp4"; json.dump(sp, open(spec, "w"))
        r = run("react-plan.py", "--spec", spec, "--public", pub)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("integral: ouvir inteira", r.stdout)
        p = load(os.path.join(d, "react-plan.json"))
        self.assertEqual([s["tipo"] for s in p["segments"]][:2], ["gancho", "trecho"])
        self.assertEqual(p["segments"][4]["layout"], "cheia")
        r = run("react-compose.py", "--plan", os.path.join(d, "react-plan.json"), "--public", pub)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        html = read(os.path.join(pub, "index.html"))
        self.assertIn('class="origcheia"', html)
        self.assertEqual(html.count('class="rea"'), 1)            # no top box during the full-screen original

    def test_long_trecho_and_low_share_fail(self):
        d, pub, spec = self.setup([[0, 15], [15, 30]], [5, 5])
        r = run("react-plan.py", "--spec", spec, "--public", pub)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("trecho 1 tem 15.0 s", r.stdout)
        self.assertIn("sua fala", r.stdout)

    def test_no_credit_fails(self):
        d, pub, spec = self.setup([[0, 8], [8, 16]], [20, 20], credito="")
        r = run("react-plan.py", "--spec", spec, "--public", pub)
        self.assertEqual(r.returncode, 1)
        self.assertIn("sem credito", r.stdout)

    def test_mismatch_and_missing_reaction(self):
        d, pub, spec = self.setup([[0, 8], [8, 16], [16, 20]], [20, 20], reacao=False)
        r = run("react-plan.py", "--spec", spec, "--public", pub)
        self.assertEqual(r.returncode, 1)
        self.assertIn("3 trechos e 2 falas", r.stdout)
        self.assertIn("sem gravacao de reacao", r.stdout)


if __name__ == "__main__":
    unittest.main()

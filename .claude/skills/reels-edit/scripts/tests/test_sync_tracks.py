"""sync-tracks.py: the reaction take (you watching, the original playing out loud) is found 2.30 s after its start."""
import json, os, unittest
from .helpers import ffmpeg, needs_ffmpeg, run, scratch


@needs_ffmpeg
class SyncTracks(unittest.TestCase):
    def test_reaction_offset(self):
        d = scratch(self)
        orig, rea = os.path.join(d, "original.mp4"), os.path.join(d, "reacao.mp4")
        # the original: a chirpy, non-periodic sound (noise through a band-pass, varying)
        ffmpeg("-f", "lavfi", "-i", "testsrc2=size=160x284:rate=30:duration=20", "-f", "lavfi", "-i", "anoisesrc=d=20:c=pink:r=48000:a=0.5:seed=7",
               "-af", "bandpass=f=900:w=600,volume='0.4+0.6*sin(2*PI*t*0.7)':eval=frame", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", orig)
        # the reaction: room noise, then the original's sound 2.30 s in, quieter (a speaker in the room)
        ffmpeg("-f", "lavfi", "-i", "testsrc2=size=160x284:rate=30:duration=25", "-i", orig, "-f", "lavfi", "-i", "anoisesrc=d=25:c=white:r=48000:a=0.03:seed=3",
               "-filter_complex", "[1:a]adelay=2300|2300,volume=0.5[o];[o][2:a]amix=inputs=2:duration=longest:normalize=0[a]",
               "-map", "0:v", "-map", "[a]", "-t", "25", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", rea)
        r = run("sync-tracks.py", "--a", rea, "--b", orig, "--window", "20")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        res = json.loads(r.stdout[r.stdout.index("{"):r.stdout.rindex("}") + 1])
        self.assertAlmostEqual(res["offset_b_after_a"], 2.30, delta=0.03)


if __name__ == "__main__":
    unittest.main()

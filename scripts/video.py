#!/usr/bin/env python3
"""
Turn a rendered slide sequence into a video.

    python3 scripts/video.py build/how-not-to-plan
    python3 scripts/video.py build/venue-myths --seconds 2.5 --music brand/audio/bed.m4a

Every slide holds for `seconds`, with a short cross fade between them. Output is
H.264 MP4, yuv420p, which is what Instagram wants for Reels and Stories.

Needs ffmpeg:  brew install ffmpeg
"""
import os, sys, glob, subprocess, shutil, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_video(d, seconds, fade, music, fps):
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is not installed. Run:  brew install ffmpeg")

    pngs = sorted(glob.glob(os.path.join(d, "*.png")))
    if not pngs:
        sys.exit(f"no PNGs in {d}. Run scripts/render.py first.")

    name = os.path.basename(d.rstrip("/"))
    out = os.path.join(ROOT, "build", f"{name}.mp4")

    # One input per slide, each held for `seconds`, chained with xfade.
    cmd = ["ffmpeg", "-y"]
    for p in pngs:
        cmd += ["-loop", "1", "-t", str(seconds), "-i", p]
    if music:
        cmd += ["-i", music]

    n = len(pngs)
    if n == 1:
        filt = "[0:v]format=yuv420p[v]"
    else:
        parts, prev, offset = [], "0:v", seconds - fade
        for i in range(1, n):
            tag = f"x{i}"
            parts.append(
                f"[{prev}][{i}:v]xfade=transition=fade:duration={fade}:offset={offset:.3f}[{tag}]"
            )
            prev, offset = tag, offset + seconds - fade
        parts.append(f"[{prev}]format=yuv420p[v]")
        filt = ";".join(parts)

    cmd += ["-filter_complex", filt, "-map", "[v]"]
    if music:
        cmd += ["-map", f"{n}:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", out]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    secs = n * seconds - (n - 1) * fade
    print(f"video  {os.path.basename(out)}  {n} slides  {secs:.1f}s")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--seconds", type=float, default=3.0, help="hold per slide")
    ap.add_argument("--fade", type=float, default=0.4, help="cross fade length")
    ap.add_argument("--music", default=None, help="optional audio bed")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    if a.fade >= a.seconds:
        sys.exit("--fade must be shorter than --seconds")
    for d in a.dirs:
        build_video(d, a.seconds, a.fade, a.music, a.fps)

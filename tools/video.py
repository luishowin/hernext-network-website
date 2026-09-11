"""Encode the looping hero clip for the home page.

Run from anywhere:   python tools/video.py

Put the camera file in "source-media/" at the repository root, which is
gitignored, and this writes two web renditions into docs/assets/video/. Those
are committed; the camera file never is. A ten second clip off an R5 is several
hundred megabytes, and git keeps every version of a binary it is given forever.

Two renditions, chosen in main.js by viewport width, because this is the single
heaviest thing on the site and a phone on mobile data should not pay desktop
weight for a decorative band. There is no audio track at all. The clip carries
no information in sound, muting is required for autoplay anyway, and a file
with no audio stream cannot raise WCAG 1.4.2 no matter how it is embedded.

H.264 in MP4 only. WebM would save some bytes on some browsers, but the site
holds itself to shipping no unused assets, and a second set of files that most
visitors never touch is hard to square with that.
"""
import os, shutil, subprocess, sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
SRC = os.path.join(ROOT, "source-media")
OUT = os.path.join(ROOT, "docs", "assets", "video")

CLIP_EXTENSIONS = (".mov", ".mp4", ".m4v", ".mkv", ".avi", ".mts", ".m2ts")

# Seconds. Long enough to read as a scene, short enough that the loop is not
# the heaviest asset on the site by an order of magnitude.
DURATION = 10
FPS = 25

# width, crf, h264 profile, byte ceiling in KB
RENDITIONS = [
    ("hnn-hero-1600.mp4", 1600, 27, "high", 1600),
    ("hnn-hero-960.mp4", 960, 30, "main", 600),
]

POSTER_FRAME = "hero-frame.png"


def ffmpeg():
    """The ffmpeg binary, or a message explaining how to get one."""
    found = shutil.which("ffmpeg")
    if not found:
        raise SystemExit(
            "ffmpeg is not installed.\n\n"
            "RPM Fusion is already enabled on this machine, so:\n"
            "    sudo dnf install ffmpeg\n\n"
            "Fedora's ffmpeg-free will not do: it has no libx264, and H.264 is\n"
            "what every browser can actually play.")
    return found


def clip():
    """The single video file in source-media/."""
    if not os.path.isdir(SRC):
        raise SystemExit("source-media/ does not exist. Create it and put the clip in it.")
    found = [f for f in sorted(os.listdir(SRC))
             if f.lower().endswith(CLIP_EXTENSIONS)]
    if not found:
        raise SystemExit(
            "No video file in source-media/.\n"
            "Drop the clip in there and run this again. Anything ffmpeg reads\n"
            "will do; it gets transcoded either way.")
    if len(found) > 1:
        raise SystemExit(
            "More than one video file in source-media/, so which one is the\n"
            "hero clip is ambiguous:\n  %s" % "\n  ".join(found))
    return os.path.join(SRC, found[0])


def run(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit("ffmpeg failed:\n%s" % result.stderr[-2000:])
    return result


def probe(path):
    """Duration, dimensions and whether the file carries any audio."""
    probe_bin = shutil.which("ffprobe")
    if not probe_bin:
        return None
    out = subprocess.run([
        probe_bin, "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,width,height",
        "-of", "default=noprint_wrappers=1", path,
    ], capture_output=True, text=True).stdout
    fields = dict(line.split("=", 1) for line in out.strip().splitlines() if "=" in line)
    return {
        "duration": float(fields.get("duration", 0)),
        "width": fields.get("width"),
        "height": fields.get("height"),
        "audio": "audio" in out,
    }


def main():
    binary = ffmpeg()
    source = clip()
    os.makedirs(OUT, exist_ok=True)

    info = probe(source)
    print("source  %s" % os.path.basename(source))
    if info:
        print("        %s x %s, %.1fs, %s"
              % (info["width"], info["height"], info["duration"],
                 "has audio (dropped)" if info["audio"] else "no audio"))
        if info["duration"] < DURATION:
            print("        shorter than %ds, so the whole clip is used" % DURATION)

    over = []
    for name, width, crf, profile, cap in RENDITIONS:
        path = os.path.join(OUT, name)
        run([
            binary, "-y", "-i", source,
            "-an",                       # no audio stream at all
            "-t", str(DURATION),
            "-vf", "scale=%d:-2:flags=lanczos,fps=%d" % (width, FPS),
            "-c:v", "libx264", "-profile:v", profile,
            "-pix_fmt", "yuv420p",       # the only chroma format Safari will decode
            "-crf", str(crf), "-preset", "slow",
            "-g", str(FPS * 2),
            "-movflags", "+faststart",   # moov atom first, so it starts on first bytes
            path,
        ])
        size = os.path.getsize(path) / 1024
        result = probe(path)
        flag = ""
        if size > cap:
            flag = "   OVER %d KB CAP" % cap
            over.append((name, crf))
        if result and result["audio"]:
            raise SystemExit("%s came out with an audio stream. That should be impossible "
                             "with -an; check the ffmpeg build." % name)
        print("  %-22s %4dw  crf %d  %7.1f KB%s" % (name, width, crf, size, flag))

    # The still behind the video is the first frame, so the crossfade from the
    # poster to the clip has nothing to cross. Feed this through images.py as
    # the hero source if you want them to agree exactly.
    frame = os.path.join(SRC, POSTER_FRAME)
    run([binary, "-y", "-i", os.path.join(OUT, RENDITIONS[0][0]),
         "-frames:v", "1", frame])
    print("  %-22s first frame, for use as the hero still" % POSTER_FRAME)

    print("\nNow run:  python tools/make.py")
    print("The home hero picks the clip up automatically once both files exist.")

    if over:
        raise SystemExit(
            "\n%d rendition(s) came in over budget. Raise the crf in RENDITIONS\n"
            "and run again, or shorten the clip: %s"
            % (len(over), ", ".join("%s at crf %d" % o for o in over)))


if __name__ == "__main__":
    main()

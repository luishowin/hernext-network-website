"""Encode the looping hero clip for the home page.

Run from anywhere:   python tools/video.py

Put the camera file in "source-media/" at the repository root, which is
gitignored, and this writes one web rendition into docs/assets/video/. That is
committed; the camera file never is. Git keeps every version of a binary it is
given, forever.

The clip is portrait, so it plays only where the hero is portrait too: on
phone-sized screens, where main.js lays it over a 4:5 cut of the hero
photograph. Wider screens keep the photograph alone and never request the file.

There is no audio track at all. The clip carries no information in sound,
muting is required for autoplay anyway, and a file with no audio stream cannot
raise WCAG 1.4.2 no matter how it is embedded.

H.264 in MP4 only. WebM would save some bytes on some browsers, but the site
holds itself to shipping no unused assets, and a second file that most
visitors never touch is hard to square with that.
"""
import os, shutil, subprocess, sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
SRC = os.path.join(ROOT, "source-media")
OUT = os.path.join(ROOT, "docs", "assets", "video")

CLIP_EXTENSIONS = (".mov", ".mp4", ".m4v", ".mkv", ".avi", ".mts", ".m2ts")

# Seconds. The supplied clip is an edit of five shots, and a team member who
# has asked not to be featured on the site yet appears in the first, second and
# fifth. Only the third and fourth are used. Their cuts fall at 2.836s and
# 7.241s, and each end is held a frame inside its cut, so rounding can never
# let a frame of a neighbouring shot through. A replacement edit needs both
# values revisiting, and the first and last frames of the output checking.
START = 2.87
DURATION = 4.33

# name, width, crf, h264 profile, byte ceiling in KB
RENDITIONS = [
    ("hnn-hero-portrait-720.mp4", 720, 28, "high", 800),
]


def ffmpeg():
    """The ffmpeg binary, or a message explaining how to get one."""
    found = shutil.which("ffmpeg")
    if not found:
        raise SystemExit(
            "ffmpeg is not installed.\n\n"
            "RPM Fusion is already enabled on this machine, so:\n"
            "    sudo dnf install ffmpeg --allowerasing\n\n"
            "--allowerasing lets it replace Fedora's *-free libav libraries,\n"
            "which conflict with it. Fedora's ffmpeg-free will not do: it has no\n"
            "libx264, and H.264 is what every browser can actually play.")
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
        print("        %s x %s, %.2fs, %s"
              % (info["width"], info["height"], info["duration"],
                 "has audio (dropped)" if info["audio"] else "no audio"))
        if info["duration"] < START + DURATION:
            raise SystemExit(
                "The clip is %.2fs long, shorter than the %.2fs to %.2fs this keeps.\n"
                "A different edit needs START and DURATION revisiting."
                % (info["duration"], START, START + DURATION))
    print("        keeping %.2fs to %.2fs" % (START, START + DURATION))

    over = []
    for name, width, crf, profile, cap in RENDITIONS:
        path = os.path.join(OUT, name)
        run([
            binary, "-y",
            "-ss", str(START),           # before -i, so the seek is frame accurate
            "-i", source,
            "-t", str(DURATION),
            "-an",                       # no audio stream at all
            # No fps filter. The source runs at 29.97, and resampling it to 25
            # drops one frame in six, which judders on a moving camera.
            "-vf", "scale=%d:-2:flags=lanczos" % width,
            "-c:v", "libx264", "-profile:v", profile,
            "-pix_fmt", "yuv420p",       # the only chroma format Safari will decode
            "-crf", str(crf), "-preset", "slow",
            "-g", "60",                  # a keyframe every two seconds
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
        print("  %-26s %4dw  crf %d  %7.1f KB%s" % (name, width, crf, size, flag))

    print("\nNow run:  python tools/make.py")
    print("The home hero picks the clip up automatically once the file exists.")

    if over:
        raise SystemExit(
            "\n%d rendition(s) came in over budget. Raise the crf in RENDITIONS\n"
            "and run again: %s"
            % (len(over), ", ".join("%s at crf %d" % o for o in over)))


if __name__ == "__main__":
    main()

"""Cut every site photograph from the untouched originals.

Run from anywhere:   python tools/images.py

The originals live in "source-media/" at the repository root, which is
gitignored; the WebP this writes into docs/assets/images/ is committed, so the
site builds and deploys without them.

The last set of photographs was produced by a throwaway snippet pasted into a
shell, and the crop boxes it used were never written down anywhere. When the
originals were later cleared off the machine, the cropped and lossily
compressed WebP became the only surviving copy, and nothing could be recut. The
manifest below exists so that cannot happen twice: source file, crop box and
output widths for all nine slots, in one place, under version control.

Crops are cut here rather than left to object-fit, so the ratio in the markup
matches the ratio in the stylesheet and the page never shifts as it loads.

Quality is searched per image rather than fixed. These frames are far busier
than the stock photography they replace, all people and plywood grain and
stacked plastic chairs, and a single quality setting that suits the calm frames
overshoots badly on the crowded ones. Each file is encoded at the highest
quality that still fits the byte cap for its width.
"""
import io, os
from PIL import Image, ImageOps

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
SRC = os.path.join(ROOT, "source-media")
OUT = os.path.join(ROOT, "docs", "assets", "images")

# Crop boxes are (left, top, width, height) in the original's pixel space, which
# is how a photographer reads a crop and how ImageMagick prints one. PIL wants
# (left, top, right, bottom); box() below converts.
#
# Every frame is from the same event, so the slots were assigned to keep any two
# images on the same page from reading as the same picture, and the crops on
# IMG_0805, IMG_0807 and IMG_0716 are deliberately tight: the first two exclude
# a small child sitting in the foreground, and the third drops a bank of empty
# chairs that swallowed the card at its rendered size.
PHOTOS = [
    # stem,            source,     crop (l, t, w, h),            widths
    ("hnn-presentation", "IMG_0713", (0, 560, 5896, 3316), (700, 1000, 1600)),
    ("hnn-office",       "IMG_0825", (0, 500, 6703, 3770), (600, 900, 1400)),
    ("hnn-forum",        "IMG_0807", (0, 380, 6905, 3021), (700, 1000, 1400)),
    ("hnn-academy",      "IMG_0778", (0, 180, 5627, 3751), (400, 800, 1200)),
    ("hnn-mentoring",    "IMG_0805", (1822, 950, 2950, 1967), (400, 800, 1200)),
    ("hnn-trade",        "IMG_0716", (3385, 2250, 3900, 2600), (400, 800, 1200)),
    ("hnn-team",         "IMG_0721", (0, 400, 7285, 4857), (600, 900, 1400)),
    ("hnn-hall",         "IMG_0780", (1400, 400, 4400, 2933), (600, 900, 1400)),
    ("hnn-conversation", "IMG_0890", (1087, 0, 3260, 4075), (400, 600, 800, 1000)),

    # A second pass of frames, four of them shot square. They are kept square
    # rather than cropped into 3:2 or 4:5, which on a standing figure means
    # cutting it off at the knees or cropping the people at the edges out.
    #
    # The two outdoor frames carry an allowance. Both are full of foliage, and
    # a hedge in daylight is about the most expensive thing a photograph can
    # contain: every leaf is an edge. Held to the ordinary budget they encode
    # at quality 48, which is where artefacts start showing on skin, and the
    # faces are the subject. The allowance buys back roughly twenty points of
    # quality for about fifty kilobytes on the largest rung.
    ("hnn-together",     "IMG_0693", (0, 0, 5101, 5101), (400, 700, 1000), 1.5),
    ("hnn-welcome",      "IMG_0701", (0, 0, 4073, 4073), (400, 700, 1000), 1.5),
    ("hnn-facilitator",  "IMG_0776", (0, 0, 3197, 3197), (400, 700, 1000)),
    ("hnn-coordinator",  "IMG_0776-2", (0, 0, 2359, 2359), (400, 700, 1000)),
    ("hnn-circle",       "IMG_0750", (0, 300, 7285, 4857), (600, 900, 1400)),
]

# The social card is recut from the hero rather than being its own photograph,
# so the preview and the page a visitor lands on show the same room.
OG_SOURCE = "hnn-presentation"
OG_SIZE = (1200, 630)

# The byte ceiling is budgeted from pixel count rather than width, because the
# one portrait slot holds nearly twice the pixels of a landscape frame at the
# same width and a width-indexed table would squeeze it for no reason.
#
# It is not linear in pixels either. Downscaling concentrates detail, so cost
# per pixel climbs as a frame shrinks: the outgoing set ran about 112 KB per
# megapixel at 1600 wide and about 160 KB per megapixel at 700. An exponent of
# three quarters tracks that curve, and the constant is set so a 1600 x 900
# hero is allowed about 170 KB, near the 168 KB the calmer photograph it
# replaces actually cost.
KB_AT_ONE_MEGAPIXEL = 130
SIZE_EXPONENT = 0.75
FLOOR_KB = 16

# Below this the compression artefacts start showing on skin and on the flat
# painted walls, so a file that cannot fit its cap is reported rather than
# quietly degraded past the point where it looks cheap.
QUALITY_FLOOR = 48
QUALITY_CEILING = 82


def cap_kb(im, allowance=1.0):
    """The byte ceiling this image is allowed, from its pixel count.

    The allowance is the manifest's way of saying that a particular frame is
    genuinely harder to encode than the curve assumes, rather than quietly
    loosening the curve for everything.
    """
    megapixels = im.width * im.height / 1e6
    budget = KB_AT_ONE_MEGAPIXEL * megapixels ** SIZE_EXPONENT * allowance
    return max(FLOOR_KB, round(budget))


def box(crop):
    """A (left, top, width, height) crop as the (l, t, r, b) PIL wants."""
    left, top, width, height = crop
    return (left, top, left + width, top + height)


def load(name):
    """The original, EXIF rotation applied, in plain RGB."""
    path = os.path.join(SRC, name + ".jpg")
    if not os.path.exists(path):
        raise SystemExit(
            "%s is missing from source-media/.\n"
            "The originals are gitignored and kept local. Restore them before "
            "recutting, or the crops in this file cannot be reproduced." % name)
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def encoded(im, quality):
    """The image as WebP bytes, at the effort level the site is built with."""
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=6)
    return buf.getvalue()


def best(im, cap_kb):
    """The highest quality whose WebP still fits the cap, and those bytes.

    Bisects rather than stepping, so a 1600 wide frame costs six encodes
    instead of thirty. Returns the floor unchanged if even that overshoots;
    the caller reports it rather than shipping something it did not intend.
    """
    cap = cap_kb * 1024
    floor_bytes = encoded(im, QUALITY_FLOOR)
    if len(floor_bytes) > cap:
        return QUALITY_FLOOR, floor_bytes, False

    low, high = QUALITY_FLOOR, QUALITY_CEILING
    chosen, data = QUALITY_FLOOR, floor_bytes
    while low <= high:
        mid = (low + high) // 2
        trial = encoded(im, mid)
        if len(trial) <= cap:
            chosen, data = mid, trial
            low = mid + 1
        else:
            high = mid - 1
    return chosen, data, True


def scaled(im, width):
    """Resized to a target width, keeping the crop's own ratio."""
    height = max(1, round(im.height * width / im.width))
    return im.resize((width, height), Image.LANCZOS)


def write(data, name):
    path = os.path.join(OUT, name)
    with open(path, "wb") as f:
        f.write(data)
    return path


def main():
    if not os.path.isdir(SRC):
        raise SystemExit(
            "source-media/ does not exist. It holds the untouched originals "
            "and is gitignored; create it and put the camera files back before "
            "running this.")

    over = []
    total = 0
    hero = None

    for entry in PHOTOS:
        stem, source, crop, widths = entry[:4]
        allowance = entry[4] if len(entry) > 4 else 1.0
        original = load(source)
        cropped = original.crop(box(crop))
        if stem == OG_SOURCE:
            hero = cropped

        print("%s  from %s at %r" % (stem, source, crop))
        for width in widths:
            im = scaled(cropped, width)
            cap = cap_kb(im, allowance)
            quality, data, fitted = best(im, cap)
            name = "%s-%d.webp" % (stem, width)
            write(data, name)
            total += len(data)
            print("  %-30s %4d x %-4d  q%-3d %6.1f KB%s"
                  % (name, im.width, im.height, quality, len(data) / 1024,
                     "" if fitted else "   OVER %d KB CAP" % cap))
            if not fitted:
                over.append(name)

    # The card is cut from the hero crop rather than the original, so it frames
    # the same moment the page does, only wider.
    wide = hero.height * OG_SIZE[0] / OG_SIZE[1]
    inset = round((hero.width - wide) / 2)
    card = hero.crop((inset, 0, hero.width - inset, hero.height))
    card = card.resize(OG_SIZE, Image.LANCZOS)
    path = os.path.join(OUT, "og-image.jpg")
    card.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    size = os.path.getsize(path)
    total += size
    print("og-image.jpg  recut from the hero crop")
    print("  %-30s %4d x %-4d       %6.1f KB" % ("og-image.jpg", 1200, 630, size / 1024))

    print("\n%.2f MB across %d files"
          % (total / 1048576, sum(len(p[3]) for p in PHOTOS) + 1))
    if over:
        raise SystemExit(
            "\n%d file(s) could not reach their byte cap at quality %d: %s\n"
            "Either raise the cap in CAPS, or crop tighter so there is less "
            "detail to encode." % (len(over), QUALITY_FLOOR, ", ".join(over)))


if __name__ == "__main__":
    main()

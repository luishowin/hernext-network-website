"""Derive every site icon from the client's PNG artwork.

Run from anywhere:   python tools/icons.py

The brand SVGs carry hundreds of nested paths and are miserable to hand-edit,
so the favicons, the navbar mark and the footer lockup are all cut from the two
2000 x 2000 transparent PNGs the client supplied. Those live in "HNN Logo C/",
which is gitignored; the cropped outputs in docs/assets/images/ are committed,
so the site builds and deploys without them.

"Light Background" and "Dark Background" name the ground the artwork sits on,
not its ink. Light-background art is plum with a hollow outline ring; the dark
one is white ink with a solid plum disc, which is why it is the better favicon:
a filled shape still reads at 16 x 16, and it works on light and dark tabs.

Both files stack four blocks, separated by fully transparent rows: the emblem,
the HERNEXT NETWORK wordmark, the gold rule, and the tagline. Rather than
hardcode crop boxes, this rediscovers those blocks from the alpha channel each
run, so a re-export from the client keeps working and a changed layout fails
loudly instead of quietly producing a mis-cropped icon.
"""
import os
from PIL import Image

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
SRC = os.path.join(ROOT, "HNN Logo C", "HNN Logo Files")
OUT = os.path.join(ROOT, "docs", "assets", "images")

LIGHT = os.path.join(SRC, "HNN Logo Light Background.png")
DARK = os.path.join(SRC, "HNN Logo Dark Background.png")

# Alpha at or below this is treated as ground rather than ink, so the faint
# edge of an antialiased stroke does not smear the block boundaries.
FLOOR = 8

EMBLEM, WORDMARK, RULE, TAGLINE = range(4)

WHITE = (255, 255, 255)


def load(path):
    """The artwork, plus a hard black-and-white mask of where its ink is."""
    im = Image.open(path).convert("RGBA")
    mask = im.getchannel("A").point(lambda v: 255 if v > FLOOR else 0)
    return im, mask


def blocks(mask):
    """The stacked artwork blocks, top to bottom, as (l, t, r, b) boxes.

    A block is a run of consecutive rows holding ink. Boxes follow the PIL
    convention, so right and bottom are exclusive and can be passed to crop().
    """
    w, h = mask.size
    inked = [mask.crop((0, y, w, y + 1)).getbbox() is not None for y in range(h)]
    found, y = [], 0
    while y < h:
        if not inked[y]:
            y += 1
            continue
        top = y
        while y < h and inked[y]:
            y += 1
        # getbbox on the strip gives the horizontal extent of this block only.
        left, _, right, _ = mask.crop((0, top, w, y)).getbbox()
        found.append((left, top, right, y))
    return found


def union(boxes):
    """The smallest box containing all of them."""
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def squared(im):
    """Padded with transparency to a square, so 1:1 width/height attrs are honest."""
    side = max(im.size)
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return out


def written(im, name):
    path = os.path.join(OUT, name)
    im.save(path)
    report(path, im.size)
    return path


def report(path, size):
    kb = os.path.getsize(path) / 1024
    print("  %-24s %4d x %-4d %7.1f KB" % (os.path.basename(path), size[0], size[1], kb))


def scaled(im, height):
    """Resized to a target height, keeping the aspect ratio."""
    width = max(1, round(im.width * height / im.height))
    return im.resize((width, height), Image.LANCZOS)


def main():
    light_im, light_mask = load(LIGHT)
    dark_im, dark_mask = load(DARK)

    light_blocks = blocks(light_mask)
    dark_blocks = blocks(dark_mask)

    for name, found in (("light", light_blocks), ("dark", dark_blocks)):
        if len(found) != 4:
            raise SystemExit(
                "The %s artwork resolved to %d blocks, not the expected 4 "
                "(emblem, wordmark, rule, tagline). The client has changed the "
                "lockout layout; re-measure before trusting these crops.\n  %r"
                % (name, len(found), found))

    # The two exports are the same drawing recoloured, so the emblem must land
    # in the same place in both. If it ever does not, one file has been redrawn
    # independently and the navbar and favicon would stop agreeing.
    if light_blocks[EMBLEM] != dark_blocks[EMBLEM]:
        raise SystemExit(
            "The emblem sits at %r in the light artwork but %r in the dark one. "
            "The two exports have drifted apart."
            % (light_blocks[EMBLEM], dark_blocks[EMBLEM]))

    # Navbar: the hollow outline ring, matching what the site shows today. Cut
    # square so the existing width="44" height="44" stays exact.
    nav = squared(light_im.crop(light_blocks[EMBLEM]))

    # Favicons: the solid plum disc, which survives being shrunk to 16 px.
    badge = squared(dark_im.crop(dark_blocks[EMBLEM]))

    # Footer: emblem through the gold rule, stopping short of the tagline,
    # because the footer already prints that line as selectable HTML text.
    lockup = dark_im.crop(union(dark_blocks[EMBLEM:RULE + 1]))

    print("Cut from the client artwork:")
    print("  emblem  %r" % (dark_blocks[EMBLEM],))
    print("  lockup  %r  (tagline at %r dropped)"
          % (union(dark_blocks[EMBLEM:RULE + 1]), dark_blocks[TAGLINE]))
    print("Writing to docs/assets/images/:")

    # 4x the rendered size in style.css, which covers a device pixel ratio of 3
    # with room to spare. .brand img is 2.75rem, .site-footer__brand img 3.25rem.
    written(nav.resize((176, 176), Image.LANCZOS), "logo-mark.png")
    written(scaled(lockup, 208), "logo-lockup-dark.png")

    written(badge.resize((96, 96), Image.LANCZOS), "favicon-96.png")
    written(badge.resize((192, 192), Image.LANCZOS), "icon-192.png")
    written(badge.resize((512, 512), Image.LANCZOS), "icon-512.png")

    # A multi-resolution .ico still earns its place: it is what Windows uses for
    # pinned sites and what older browsers reach for first.
    ico = os.path.join(OUT, "favicon.ico")
    badge.resize((256, 256), Image.LANCZOS).save(
        ico, sizes=[(16, 16), (32, 32), (48, 48)])
    report(ico, (48, 48))

    # iOS composites any transparency onto black and rounds the corners itself,
    # so this one gets an opaque white tile with the disc inset, matching the
    # white ground the rest of the site is built on.
    tile = Image.new("RGB", (180, 180), WHITE)
    disc = badge.resize((144, 144), Image.LANCZOS)
    tile.paste(disc, (18, 18), disc)
    written(tile, "apple-touch-icon.png")


if __name__ == "__main__":
    main()

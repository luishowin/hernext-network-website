"""Preview the built site locally.

Run from anywhere:   python tools/serve.py        then open http://localhost:8123

This exists for one reason: `python -m http.server` does not implement range
requests. It answers every request with 200 and the whole file, and never sends
an Accept-Ranges header. A browser's media pipeline needs ranges to seek, so
the home hero clip silently hangs at readyState 0 and the page looks broken in
a way that has nothing to do with the site. Every real host, GitHub Pages
included, serves ranges correctly.

Nothing here is deployed. It is a preview server for local work, in the same
spirit as tools/make.py: a convenience, not a build step.
"""
import functools, http.server, os, re, socketserver, sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
DOCS = os.path.join(ROOT, "docs")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8123

RANGE = re.compile(r"bytes=(\d*)-(\d*)")


class Handler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler, plus the single byte range form browsers send."""

    def send_head(self):
        header = self.headers.get("Range")
        if not header:
            return super().send_head()

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404)
            return None

        size = os.fstat(f.fileno()).st_size
        match = RANGE.fullmatch(header.strip())
        if not match:
            f.close()
            self.send_error(400, "Malformed Range")
            return None

        start, end = match.group(1), match.group(2)
        if start:
            start = int(start)
            end = int(end) if end else size - 1
        else:
            # A suffix range, "bytes=-500", means the last 500 bytes.
            start, end = max(0, size - int(end)), size - 1
        end = min(end, size - 1)

        if start >= size or start > end:
            f.close()
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % size)
            self.end_headers()
            return None

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        f.seek(start)
        return Ranged(f, end - start + 1)

    def end_headers(self):
        # Preview only, so an edited file is never served from cache while you
        # are trying to work out why your change did nothing.
        #
        # Media is the exception and has to be no-cache rather than no-store. A
        # no-store response cannot enter Chrome's media cache, and its video
        # pipeline then sits at readyState 0 for ever, with no error raised and
        # nothing in the console to explain it.
        media = self.path.rsplit(".", 1)[-1].lower() in ("mp4", "webm", "mov", "m4v", "ogg")
        self.send_header("Cache-Control", "no-cache" if media else "no-store")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "304" not in fmt % args:
            super().log_message(fmt, *args)


class Ranged:
    """A file object that stops after the requested number of bytes."""

    def __init__(self, f, length):
        self.f, self.left = f, length

    def read(self, n=-1):
        if self.left <= 0:
            return b""
        data = self.f.read(self.left if n < 0 else min(n, self.left))
        self.left -= len(data)
        return data

    def close(self):
        self.f.close()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    if not os.path.isdir(DOCS):
        raise SystemExit("docs/ does not exist. Run python tools/make.py first.")
    handler = functools.partial(Handler, directory=DOCS)
    with Server(("", PORT), handler) as httpd:
        print("serving docs/ with range support on http://localhost:%d" % PORT)
        print("ctrl-c to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()

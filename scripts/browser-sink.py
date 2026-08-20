"""Tiny localhost sink so a browser tab can hand a file to disk.

The Izumo chart lives on shinto.miraheze.org, which answers curl and every other
non-browser client with a bot-check page, so the only client that can read it is
the Chrome tab. Tool output truncates around a kilobyte, which makes printing a
10 KB roster through the transcript a dozen round-trips. This closes the gap: the
page POSTs its text here and it lands in reports/.

    python scripts/browser-sink.py --out reports/izumo-chart-roster.tsv

Then from the page:

    fetch('http://127.0.0.1:8731/', {method:'POST', mode:'no-cors', body: text})

no-cors is deliberate - the response is opaque and unreadable to the page, which
is all the page needs, and it avoids a preflight. Serves exactly one request and
exits, so nothing is left listening.
"""

import argparse
import http.server
import pathlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
parser.add_argument("--port", type=int, default=8731)
args = parser.parse_args()

out = pathlib.Path(args.out)


class Sink(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(body)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        print(f"wrote {len(body)} bytes to {out}", file=sys.stderr)
        self.server.done = True

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", args.port), Sink)
srv.done = False
while not srv.done:
    srv.handle_request()

#!/usr/bin/env python3
"""Render the PIP stacks dashboard.

Reads the global store (default ~/.pip/state.json), injects it into the
self-contained dashboard template, and writes a standalone HTML file the user
can open in any browser. Pure standard library — no dependencies.

Usage:
    python3 render_dashboard.py [--state PATH] [--out PATH] [--open]

Defaults:
    --state  ~/.pip/state.json
    template <this script>/../assets/dashboard.html
    --out    ~/.pip/dashboard.html
"""
import argparse, json, os, re, sys, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "dashboard.html")
DATA_RE = re.compile(
    r'(<script id="pip-data" type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default=os.path.expanduser("~/.pip/state.json"))
    ap.add_argument("--out", default=os.path.expanduser("~/.pip/dashboard.html"))
    ap.add_argument("--template", default=TEMPLATE)
    ap.add_argument("--open", action="store_true", help="open in the default browser")
    args = ap.parse_args()

    with open(args.template, "r", encoding="utf-8") as f:
        template = f.read()

    if os.path.exists(args.state):
        with open(args.state, "r", encoding="utf-8") as f:
            data = json.load(f)  # validate
        payload = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        # No store yet → keep the template's embedded demo data so the dashboard
        # still renders. PIP populates ~/.pip/state.json as concepts get learned.
        print(f"note: {args.state} not found — rendering with template demo data.",
              file=sys.stderr)
        payload = None

    out_html = template
    if payload is not None:
        # guard the replacement against backref/escape surprises
        out_html = DATA_RE.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3),
                               template, count=1)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out_html)

    print(args.out)
    if args.open:
        webbrowser.open("file://" + os.path.abspath(args.out))


if __name__ == "__main__":
    main()

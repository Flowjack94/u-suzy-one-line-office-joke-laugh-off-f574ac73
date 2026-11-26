"""Validate the one-line office joke entry and write it to /output/entry.txt.

Rules (this competition): the entry is exactly one line, at most 200
characters, with no control characters, no leading or trailing
whitespace, and no byte-order mark. The entry text is read from
entry.txt next to this file, validated, written verbatim to
/output/entry.txt, and verified by a round-trip read plus a byte-level
digest comparison of the two files on disk.
"""

import hashlib
import os
import sys

ENTRY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
OUTPUT_FILE = "/output/entry.txt"
MAX_CHARS = 200


def main() -> int:
    with open(ENTRY_FILE, encoding="utf-8") as f:
        text = f.read()
    # Strip exactly one trailing newline for validation; the entry is one line.
    body = text[:-1] if text.endswith("\n") else text
    if "\n" in body or "\r" in body:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(body) > MAX_CHARS:
        print(f"error: entry is {len(body)} chars, max is {MAX_CHARS}", file=sys.stderr)
        return 1
    if any(ord(c) < 32 and c not in ("\t",) for c in body):
        print("error: entry contains control characters", file=sys.stderr)
        return 1
    if not body.strip():
        print("error: entry is empty", file=sys.stderr)
        return 1
    if text.startswith("\ufeff"):
        print("error: entry starts with a BOM", file=sys.stderr)
        return 1
    if body != body.strip():
        print("error: entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    with open(OUTPUT_FILE, encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("error: round-trip verification failed", file=sys.stderr)
        return 1
    # Byte-level digest check: hash both files on disk and require equality,
    # so an encoding or newline translation on write is caught even if the
    # in-memory strings happen to compare equal.
    with open(ENTRY_FILE, "rb") as f:
        source_digest = hashlib.sha256(f.read()).hexdigest()
    with open(OUTPUT_FILE, "rb") as f:
        output_digest = hashlib.sha256(f.read()).hexdigest()
    if output_digest != source_digest:
        print("error: output digest does not match entry digest", file=sys.stderr)
        return 1
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"entry: {body}")
    print(f"chars: {len(body)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

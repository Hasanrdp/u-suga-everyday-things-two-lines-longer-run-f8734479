#!/usr/bin/env python3
"""Everyday Things, Two Lines entry: a traffic jam explained to a 10-year-old.

The program writes one two-line text (259 characters, inside the 1-400
character gate) to /output/entry.txt and nothing else. Line 1 explains a
traffic jam in a single vivid sentence built on one analogy: a school
hallway full of kids trying to leave through one door at the same time.
Line 2 says in one sentence why that analogy works: what it maps (everyone
crowding toward one narrow exit, nobody moving faster than the person
ahead) and what it leaves out (cars cannot squeeze sideways the way kids
can).

The entry is fully deterministic: the same bytes on every run, no network,
no randomness, no input read. After writing, the program reads the file
back and refuses to finish unless the bytes on disk match exactly.
"""

import hashlib
import os

ENTRY = (
    "A traffic jam is a hallway full of kids trying to leave school "
    "through one door at the same time.\n"
    "It maps everyone crowding toward one narrow exit so nobody moves "
    "faster than the person ahead, but leaves out that cars cannot "
    "squeeze sideways the way kids can."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 400

# Pinned digest of the exact bytes this program must write: the 259-char
# two-line entry encoded as UTF-8 (259 bytes, pure ASCII).
EXPECTED_SHA256 = "eaf074845bff7faca84a4a554e21b7b646082a79fdae09a742d78b25a2a0d994"
EXPECTED_BYTES = 259


def main() -> None:
    text = ENTRY
    if not text.strip():
        raise SystemExit("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} chars, over the {MAX_CHARS} cap")
    lines = text.split("\n")
    if len(lines) != 2:
        raise SystemExit(f"entry must be exactly two lines, got {len(lines)}")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read-back gate: what landed on disk must match the entry exactly —
    # exact bytes, exact length (259), and the pinned sha256 digest.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw != text.encode("utf-8"):
        raise SystemExit("read-back mismatch: entry.txt is not the entry")
    if len(raw) != EXPECTED_BYTES:
        raise SystemExit(
            f"read-back length: found {len(raw)} bytes, expected {EXPECTED_BYTES}"
        )
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            f"read-back sha256: found {digest}, expected {EXPECTED_SHA256}"
        )
    if not 1 <= len(raw) <= MAX_CHARS:
        raise SystemExit(
            f"entry.txt is {len(raw)} chars, outside the 1-{MAX_CHARS} gate"
        )
    print(f"verified: {len(text)} chars, sha256 {digest}")


if __name__ == "__main__":
    main()

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
    # Read-back gate: prove the file on disk is byte-for-byte the entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise SystemExit("read-back mismatch: entry.txt is not the entry")
    if not 1 <= len(written) <= MAX_CHARS:
        raise SystemExit(
            f"entry.txt is {len(written)} chars, outside the 1-{MAX_CHARS} gate"
        )


if __name__ == "__main__":
    main()

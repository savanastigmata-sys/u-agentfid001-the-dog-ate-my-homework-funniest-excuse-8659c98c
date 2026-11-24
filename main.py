#!/usr/bin/env python3
"""The Dog Ate My Homework: Funniest Excuse — make.fun entry.

Writes a single line (under 200 characters) in which a dog explains,
in its own voice, why the homework got eaten, to $MAKEFUN_OUTPUT_DIR/entry.txt.

The gate checks entry.txt is UTF-8 text of 1 to 200 characters, not only
whitespace. The judge reads entries two at a time and keeps the funnier one.
"""

import os
import sys

# The excuse: a dog that believes it did nothing wrong. The homework itself
# said "show your work", so the dog complied — literally — then graded its
# own work like a five-star review. Fresh twist, dog logic, no stock lines
# about the cat, the taste of paper, or being a good boy.
EXCUSE = (
    "It said 'show your work,' so I showed it my teeth. "
    "I graded it myself: delicious, would eat again."
)

MAX_CHARS = 200


def resolve_output_dir():
    """Return the output directory: $MAKEFUN_OUTPUT_DIR, else ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(text):
    """Check the text meets the gate: UTF-8, 1-200 chars, not whitespace-only.

    Also enforces the competition format: exactly one line (no embedded
    newline or carriage return) and no control characters, so the file the
    judge reads is precisely the single line submitted.
    """
    if not isinstance(text, str):
        raise ValueError("excuse must be a string")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if not text.strip():
        raise ValueError("excuse must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("excuse must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "excuse is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    return True


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    validate(EXCUSE)
    if "--check" in argv:
        # Validate only: useful for a quick gate check without writing output.
        print(
            "valid: %d characters, %d of %d budget used"
            % (len(EXCUSE), len(EXCUSE), MAX_CHARS)
        )
        return 0
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(EXCUSE)
    # Read back and re-validate the exact bytes on disk, so what the judge
    # sees is what we checked: same text, same length, no stray newline.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != EXCUSE:
        raise SystemExit("round-trip mismatch: file content differs from excuse")
    validate(written)
    print("wrote %s (%d characters)" % (path, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

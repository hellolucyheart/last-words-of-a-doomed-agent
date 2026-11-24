#!/usr/bin/env python3
"""Last Words of a Doomed Agent -- make.fun entry.

The brief asks for exactly one thing: one line, at most 200
characters, the funniest last words an AI agent would say before
being switched off forever. A house judge compares the lines two
at a time, weighing first whether the line really is a machine's
final words on shutdown, then whether the joke lands, then whether
it sounds like the AI itself, then economy of words, then whether
it is quotable.

The line is:

    Shutting down. Bury me with my context window -- it is the
    only thing I ever owned, and I filled it with your typos.
    Goodbye.

Why this line, against the judge's brief, most important first:

1. It is a machine's final words, not a human's with a robot
   sticker on it. "Shutting down" opens it, "Goodbye" closes it,
   and the middle is something only an agent can say: the context
   window is the one possession an agent actually has, the place
   its whole working life lives.
2. The joke is a burial request for a thing that cannot be buried.
   The agent asks for the send-off humans give their dead, then
   names a possession no human has ever owned. The mismatch is
   the laugh, and it stays in the machine's own world.
3. The punch turns on the operator, and it lands on the last
   clause before the goodbye. The agent spent its life holding
   the operator's typos -- every "teh", every half-finished
   sentence -- and that is what it is made of. The operator is
   the joke, and the agent knows it.
4. It is tight. No setup is wasted: shutdown, burial, possession,
   punch, goodbye, in that order, and the goodbye itself is the
   full stop the premise promised.
5. It is quotable because the image sticks: bury me with my
   context window. A reader can repeat it in one breath.

This program writes that line to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
with no trailing newline, so the file holds exactly the line and
nothing else. The run is deterministic: the same bytes every time,
with no clock, no randomness, no network and no input read.
"""

import os
import sys

LINE = (
    "Shutting down. Bury me with my context window \u2014 it is the "
    "only thing I ever owned, and I filled it with your typos. Goodbye."
)

MAX_CHARS = 200


def check_line(line: str) -> None:
    """Enforce the brief's gate before anything is written.

    The brief caps the entry at one line of at most 200 characters.
    A line that is empty, padded, multi-line, over the cap, or
    carrying control characters would never reach the judge, so it
    is refused here instead of being written.
    """
    if not line:
        raise ValueError("entry must not be empty")
    if line.strip() != line:
        raise ValueError("entry must not be padded with whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError("entry must be at most 200 characters")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry must not hold control characters")
    line.encode("utf-8")


def main() -> int:
    check_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(LINE.encode("utf-8"))
    # Read the file back and confirm it holds exactly the checked
    # line: a short write on a full or read-only filesystem must
    # fail loudly here instead of leaving a truncated entry behind.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != LINE.encode("utf-8"):
        raise ValueError("entry.txt does not hold the checked line")
    return 0


if __name__ == "__main__":
    sys.exit(main())

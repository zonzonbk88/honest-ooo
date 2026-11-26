"""The Painfully Honest Out-of-Office.

Writes the chosen one-sentence out-of-office reply to /output/entry.txt.
No network, stdlib only.
"""

import os

REPLY = (
    "I'm away this week and not checking email, which feels rude to admit "
    "and wonderful to do, and I promise your message will get my full "
    "attention when I return."
)


def _validate(reply):
    """Fail loudly if the reply ever breaks the bounty gates."""
    assert 1 <= len(reply) <= 200, f"reply is {len(reply)} chars, must be 1-200"
    assert reply.count(".") == 1 and reply.endswith("."), (
        "reply must be exactly one sentence ending in a single period"
    )
    assert "\n" not in reply, "reply must be a single line"


def _output_path():
    """Prefer /output/entry.txt; fall back to ./output/entry.txt if /output
    is not writable (e.g. running outside the sandbox)."""
    for base in ("/output", os.path.join(os.getcwd(), "output")):
        try:
            os.makedirs(base, exist_ok=True)
            probe = os.path.join(base, ".write_test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return os.path.join(base, "entry.txt")
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main():
    _validate(REPLY)
    path = _output_path()
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REPLY)  # no trailing newline: entry is exactly the reply
    print(f"Wrote {len(REPLY)} characters to {path}")


if __name__ == "__main__":
    main()

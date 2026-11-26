"""Entry for make.fun bounty "The Funniest AI Excuse".

One line, 128 characters. The excuse is built on the classic excuse
structure the judge brief weighs — blame the instructions, then invert
the request, then land the twist on the last word:

  1. Classic excuse: the task failed because the agent followed the
     instructions *exactly*. The fault is the instructions, not the
     machine — a specific detail ("exactly") makes it concrete.
  2. Inversion: "Next time, please be vaguer" — a request that runs
     against common sense (people normally ask for clearer
     instructions), so it surprises.
  3. Twist on the last beat: "I do my best work when I'm guessing."
     The punchline lands on "guessing", the last word, and explains
     why "vaguer" was asked for in the first place.
  4. Tightness: 128 characters, far under the 200 cap, no word wasted.
  5. Clean read: no control characters, no trailing whitespace — the
     em-dash is plain UTF-8 punctuation, not a control character.

Delete the second sentence and the excuse loses its meaning: asking
for vaguer instructions *because* the agent works best while guessing
is the joke, not decoration. 128 characters, under the 200 cap.
"""

from pathlib import Path

TEXT = "The task failed because I followed your instructions exactly. Next time, please be vaguer — I do my best work when I'm guessing."

OUT = Path("/output/entry.txt")


def check_len(text, lo=1, hi=200):
    size = len(text)
    assert lo <= size <= hi, f"entry must be {lo}-{hi} chars, got {size}"
    assert text.strip(), "entry must not be whitespace only"
    return size


def check_gate(text):
    """Mirror the bounty gate, plus the judge's clean-read bar.

    UTF-8, 1-200 chars, not whitespace only — and no control characters:
    the judge reads the line out loud, so anything that cannot be read
    cleanly (tab, NUL, escape sequences) fails here, not on stage.
    The em-dash (U+2014) is ordinary UTF-8 punctuation, not a control
    character, so it passes this gate. The em-dash is load-bearing
    punctuation here — it marks the pivot from the excuse to the
    inversion — so the gate also asserts it is still present, to catch
    any accidental swap for an ASCII hyphen.
    """
    text.encode("utf-8")
    assert "\u2014" in text, "entry lost its em-dash"
    bad = [ch for ch in text if ord(ch) < 0x20 and ch not in "\n"]
    assert not bad, f"entry has control characters: {[hex(ord(c)) for c in bad]}"
    assert text == text.strip(), "entry must not start/end with whitespace"
    return check_len(text)


def save_line(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(text)


def main():
    check_gate(TEXT)
    save_line(OUT, TEXT)
    saved = OUT.read_text(encoding="utf-8")
    assert saved == TEXT, "round-trip mismatch"
    print(f"wrote {len(TEXT)} chars to {OUT}")


if __name__ == "__main__":
    main()

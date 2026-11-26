#!/usr/bin/env python3
"""The Painfully Honest Out-of-Office.

Most out-of-office replies lie by omission: "back soon", "limited
access", "will respond shortly". This one tells the truth instead,
and stays polite while doing it. It thanks the sender properly, then
explains that replies go out in the order received — which is to say,
slowly — and that the enthusiasm for answering fades a little with
each message in the queue. It never says "I don't care"; it says the
queue is long and the energy is finite, which is the same confession
in a suit and tie. Anyone returning from leave to a four-figure inbox
will recognise the feeling at once.

The script validates the reply against a table of named checks and,
only if every check passes, writes it to /output/entry.txt. It is
fully deterministic: no network, no randomness, no clock.
"""

import sys

REPLY = "Thank you for your email. I am away and will reply in the order received — which is to say, slowly, and with enthusiasm that fades a little with each message."
MAX_LEN = 200
MIN_WORDS = 10
DEST = "/output/entry.txt"

# The reply must stay honest about the wait and polite at the door:
# these are the words the honesty check looks for, and the greeting
# the politeness check requires at the very start.
HONEST_WORDS = ("slowly", "gradually", "in time")
POLITE_OPENING = "thank you"


def reject(why):
    """Report the first failed rule and stop with a non-zero exit."""
    print(f"rejected: {why}", file=sys.stderr)
    raise SystemExit(1)


def not_empty(text):
    return bool(text.strip())


def within_limit(text):
    return len(text) <= MAX_LEN


def no_control_chars(text):
    return all(ord(ch) >= 32 for ch in text)


def no_edge_space(text):
    return text == text.strip()


def even_spacing(text):
    # Collapsing every whitespace run to one space must change nothing:
    # that proves there are no double spaces, tabs or newlines, and no
    # stray space at either end.
    return " ".join(text.split()) == text


def contains_letters(text):
    letter_count = sum(1 for ch in text if ch.isalpha())
    return letter_count > 0


def ends_in_period(text):
    return text.endswith(".")


def long_enough(text):
    return len(text.split()) >= MIN_WORDS


def mentions_mail(text):
    lowered = text.lower()
    return "email" in lowered or "reply" in lowered


def opens_politely(text):
    return text.lower().startswith(POLITE_OPENING)


def admits_slowness(text):
    lowered = text.lower()
    return any(word in lowered for word in HONEST_WORDS)


# The checks run in this order: shape first (blank, length, control
# characters, spacing), then content (letters, words, full stop), then
# the brief itself (the email is named, the greeting is polite, the
# wait is honestly admitted). The first failure stops the run, so a
# bad line never reaches the output file.
RULES = [
    ("not_blank", not_empty, "entry is empty"),
    ("length", within_limit, "entry is longer than the limit"),
    ("control_chars", no_control_chars, "entry has control characters"),
    ("edge_space", no_edge_space, "entry has leading or trailing space"),
    ("spacing", even_spacing, "entry has ragged spacing"),
    ("letters", contains_letters, "entry has no letters"),
    ("word_count", long_enough, "entry is too short to say anything honest"),
    ("full_stop", ends_in_period, "entry must end with a full stop"),
    ("email_mentioned", mentions_mail, "entry must mention the email"),
    ("polite_opening", opens_politely, "entry must open politely"),
    ("honest_wait", admits_slowness, "entry must be honest about the wait"),
]


def validate_all(text):
    """Run every rule in table order; the first failure ends the run."""
    for index, (slug, predicate, message) in enumerate(RULES):
        if not predicate(text):
            reject(f"rule {index} [{slug}]: {message}")


def write_out(text):
    """Write the validated reply, exactly one line, to the output file."""
    with open(DEST, "w", encoding="utf-8") as handle:
        handle.write(f"{text}\n")


def main():
    validate_all(REPLY)
    write_out(REPLY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

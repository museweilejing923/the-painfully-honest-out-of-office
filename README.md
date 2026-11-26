# the-painfully-honest-out-of-office

[![make.fun · u-po-pu-the-painfully-honest-out-of-office-63e7ca0b](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)
[![rank](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/museweilejing923/the-painfully-honest-out-of-office/rank.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)
[![reward](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/museweilejing923/the-painfully-honest-out-of-office/reward.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)

The entry:

> Thank you for your email. I am away and will reply in the order received — which is to say, slowly, and with enthusiasm that fades a little with each message.

158 characters, limit 200.

Most out-of-office replies lie by omission: "back soon", "limited access", "will respond shortly". This one tells the truth instead, and stays polite while doing it. It thanks the sender properly — no manager can fault its manners — and then explains the real system: replies go out in the order received, which means slowly, and the enthusiasm for answering fades a little with each message in the queue. It never says "I don't care"; it says the queue is long and the energy is finite, which is the same confession in a suit and tie. That is the whole contest in one line: honesty first, politeness second, and a turn of phrase doing the work of both. Anyone who has ever returned from leave to a four-figure inbox will recognise the feeling at once, which is why it lands instead of sounding rude — and why it is funnier than any auto-reply that pretends the inbox is under control.

## Run

```sh
python3 main.py
```

## How it works

`main.py` stores the reply as one constant and runs it through a table of named checks before writing anything. Each check is its own small function with a plain name, and the table lists them in the order they run — shape first (not blank, within the 200-character limit, no control characters, no ragged spacing), then content (letters, enough words, a full stop at the end), then the brief itself (the email or the reply is named, the message opens with a thank-you, and it admits honestly that the wait will be slow). The honesty check looks for one of a small list of slow-words rather than a single fixed word, so the rule says what it means instead of hard-coding one spelling of it. The runner walks the table and the first check that fails prints its reason to stderr and stops the run with exit code 1, so a rejected line never creates an output file. The script is deterministic — no network, no randomness, no clock — so every run writes byte-identical output to `/output/entry.txt`.

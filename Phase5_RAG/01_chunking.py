"""
Phase 5.1 - Recursive chunking.

Splits text on the highest-priority separator that fits, falling back
to finer ones. Preserves structure (paragraphs > sentences > words).
"""

from typing import List

SEPARATORS = ["\n\n", "\n", ". ", " "]


def split(text: str, max_chars: int = 600, seps: List[str] = SEPARATORS) -> List[str]:
    if len(text) <= max_chars:
        return [text.strip()]
    sep = seps[0] if seps else ""
    parts = text.split(sep) if sep else list(text)
    chunks, buf = [], ""
    for p in parts:
        candidate = (buf + sep + p) if buf else p
        if len(candidate) <= max_chars:
            buf = candidate
        else:
            if buf:
                chunks.append(buf.strip())
            if len(p) > max_chars and len(seps) > 1:
                chunks.extend(split(p, max_chars, seps[1:]))
                buf = ""
            else:
                buf = p
    if buf:
        chunks.append(buf.strip())
    return [c for c in chunks if c]


if __name__ == "__main__":
    sample = """# Reset MFA on a lost phone

If you've lost the phone with your Microsoft Authenticator app, follow these steps.

## Step 1 - Call the helpdesk

Dial 1234. Have your employee ID ready. You'll be asked 3 verification questions.

## Step 2 - Identity verification

The agent will verify your identity using HR records. This typically takes 5 minutes.

## Step 3 - MFA re-enrollment

Once verified, you'll receive a one-time code by email. Use it at https://aka.ms/mfasetup
to register a new device. Old device is automatically revoked.

If you are travelling, mention that to the agent for an expedited path."""
    for i, c in enumerate(split(sample, max_chars=300)):
        print(f"--- chunk {i} ({len(c)} chars) ---\n{c}\n")

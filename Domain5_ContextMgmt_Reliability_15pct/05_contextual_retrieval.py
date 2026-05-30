"""
Phase 5.5 - Contextual retrieval (Anthropic's trick).

For each chunk we ask Claude:
  "Given this WHOLE document and this CHUNK, write a 1-paragraph context
   that situates this chunk for retrieval."
Then we prepend that paragraph to the chunk text BEFORE embedding/BM25.
Retrieval recall typically improves ~50%.

Prompt caching makes this cheap: we put the whole document in a cached
block, then loop over chunks - subsequent calls are ~90% cheaper.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

DOCUMENT = """# Quarterly Financial Report - Q3 2026

## ARR by segment
Total ARR grew 18% YoY to $4.2B. Enterprise segment contributed $2.9B
(+22% YoY), Mid-market $0.9B (+14%), SMB $0.4B (+8%). Net dollar
retention was 117% across all segments.

## Operating expenses
R&D spend climbed to $810M (19% of revenue) reflecting AI investment.
S&M efficiency improved: payback period dropped from 22 to 18 months.

## Outlook
Q4 guidance: ARR $4.4B at midpoint. FY27 we plan to invest in EU
data residency, with capex of ~$300M for new Frankfurt and Madrid
regions.
"""

CHUNKS = [
    "Total ARR grew 18% YoY to $4.2B. Enterprise contributed $2.9B (+22% YoY).",
    "R&D spend climbed to $810M (19% of revenue) reflecting AI investment.",
    "Q4 guidance: ARR $4.4B at midpoint. FY27 capex ~$300M for EU regions.",
]

CTX_PROMPT = """<document>
{doc}
</document>

Here is a chunk we want to situate within the whole document:

<chunk>
{chunk}
</chunk>

Please give a short (<=80 tokens) context that situates this chunk for
search retrieval. Answer with ONLY the context, no preamble."""


def contextualize(chunk: str) -> str:
    resp = client.messages.create(
        model="claude-haiku-4-5",   # cheap is fine
        max_tokens=120,
        temperature=0,
        # Cache the document section so reuse is ~90% cheaper
        system=[{
            "type": "text",
            "text": "You produce short retrieval-friendly context blurbs.",
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": CTX_PROMPT.format(doc=DOCUMENT, chunk=chunk),
                "cache_control": {"type": "ephemeral"},
            }],
        }],
    )
    return resp.content[0].text.strip()


for c in CHUNKS:
    ctx = contextualize(c)
    print(">> chunk     :", c)
    print(">> context   :", ctx)
    print(">> enriched  :", ctx + " " + c)
    print()

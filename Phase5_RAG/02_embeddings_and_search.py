"""
Phase 5.2 - Embeddings + cosine similarity search.

Uses Voyage AI (Anthropic's recommended embeddings partner). If you
don't want to sign up, swap embed_voyage for any other embedding API.
"""

import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

try:
    import voyageai
    vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))
except Exception:
    vo = None


def embed_voyage(texts, input_type="document"):
    if vo is None:
        raise RuntimeError("Install voyageai and set VOYAGE_API_KEY in .env")
    return np.array(
        vo.embed(texts, model="voyage-3-large", input_type=input_type).embeddings,
        dtype=np.float32,
    )


def cosine(a, b):
    a = a / (np.linalg.norm(a, axis=-1, keepdims=True) + 1e-9)
    b = b / (np.linalg.norm(b, axis=-1, keepdims=True) + 1e-9)
    return a @ b.T


DOCS = [
    "If you lost your phone, call helpdesk at 1234 to reset MFA.",
    "Outlook calendar sync issue on macOS: disable iCloud calendar.",
    "VPN disconnects after 60s. Increase keep-alive interval to 30s.",
    "Submit holiday requests via Workday > Time Off.",
    "Order a replacement laptop via the asset portal.",
]
QUERY = "I dropped my phone, can't get into email"


def main():
    doc_vecs = embed_voyage(DOCS, input_type="document")
    q_vec = embed_voyage([QUERY], input_type="query")
    sims = cosine(q_vec, doc_vecs)[0]
    order = sims.argsort()[::-1]
    for i in order:
        print(f"{sims[i]:.3f}  {DOCS[i]}")


if __name__ == "__main__":
    main()

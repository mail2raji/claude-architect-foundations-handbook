"""
Phase 5.3 - Hybrid search: BM25 (keyword) + vector, fused with RRF.

Why hybrid?
- vector excels at semantic ("phone dead" vs "lost phone")
- BM25 excels at exact terms ("INC1042", "Outlook 365")
- RRF (Reciprocal Rank Fusion) is the simplest principled way to combine.
"""

import os
import numpy as np
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv

load_dotenv()

try:
    import voyageai
    vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))
except Exception:
    vo = None


DOCS = [
    "If you lost your phone, call helpdesk at 1234 to reset MFA.",
    "Outlook calendar sync issue on macOS: disable iCloud calendar.",
    "VPN disconnects after 60s. Increase keep-alive interval to 30s.",
    "Submit holiday requests via Workday > Time Off.",
    "Order a replacement laptop via the asset portal.",
    "Error code INC1042: kerberos clock skew over 5 minutes.",
]


def embed(texts, input_type):
    return np.array(vo.embed(texts, model="voyage-3-large",
                             input_type=input_type).embeddings, dtype=np.float32)


def normalize(v): return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-9)


def rrf(rank_lists, k=60):
    """Reciprocal Rank Fusion. rank_lists: list of [doc_ids ordered best→worst]."""
    score = {}
    for ranks in rank_lists:
        for r, doc_id in enumerate(ranks):
            score[doc_id] = score.get(doc_id, 0.0) + 1.0 / (k + r + 1)
    return sorted(score.items(), key=lambda x: x[1], reverse=True)


def main():
    # vector
    dv = normalize(embed(DOCS, "document"))
    # bm25
    tokens = [d.lower().split() for d in DOCS]
    bm25 = BM25Okapi(tokens)

    query = "INC1042 kerberos issue"
    qv = normalize(embed([query], "query"))
    sims = (qv @ dv.T)[0]
    bm25_scores = bm25.get_scores(query.lower().split())

    vec_rank  = list(np.argsort(sims)[::-1])
    bm25_rank = list(np.argsort(bm25_scores)[::-1])

    print("Vector top:", [DOCS[i][:40] for i in vec_rank[:3]])
    print("BM25   top:", [DOCS[i][:40] for i in bm25_rank[:3]])

    fused = rrf([vec_rank, bm25_rank])
    print("\nFused top:")
    for doc_id, s in fused[:3]:
        print(f"  {s:.3f}  {DOCS[doc_id]}")


if __name__ == "__main__":
    main()

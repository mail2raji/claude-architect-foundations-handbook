"""
Phase 5.4 - Reranking.

A cross-encoder reranker reads (query, candidate_text) TOGETHER and
returns a relevance score. Much better than cosine on its own, but
expensive — so you only rerank the top-25 from retrieval, keep top-5.
"""

import os
from dotenv import load_dotenv

load_dotenv()

import voyageai
vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))

CANDIDATES = [
    "If you lost your phone, call helpdesk at 1234 to reset MFA.",
    "Outlook calendar sync issue on macOS: disable iCloud calendar.",
    "Error code INC1042: kerberos clock skew over 5 minutes.",
    "Order a replacement laptop via the asset portal.",
    "VPN disconnects after 60s. Increase keep-alive interval to 30s.",
]
QUERY = "My MFA is gone after I lost my phone"

result = vo.rerank(
    query=QUERY,
    documents=CANDIDATES,
    model="rerank-2",
    top_k=3,
)

for r in result.results:
    print(f"{r.relevance_score:.3f}  idx={r.index}  {CANDIDATES[r.index]}")

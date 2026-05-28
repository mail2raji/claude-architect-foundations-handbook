"""
Phase 2.6 - Vision (image content blocks).

Real-world: an architect uploads a screenshot of a network diagram and
asks Claude to spot weak points. Works with PNG/JPG/GIF/WEBP, either
URL or base64.

NOTE: replace IMAGE_URL with a real PNG/JPG URL you have rights to use,
or switch to the base64 path with a local file (commented at bottom).
"""

import base64
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/"
    "8/89/Computer_network_diagram.svg/640px-Computer_network_diagram.svg.png"
)

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "url", "url": IMAGE_URL},
                },
                {
                    "type": "text",
                    "text": (
                        "You are a network security architect. Describe the "
                        "topology in 3 bullets, then list 2 potential "
                        "security weaknesses."
                    ),
                },
            ],
        }
    ],
)

print(resp.content[0].text)


# ---- ALTERNATIVE: local file via base64 ----
# img_path = Path("diagram.png")
# b64 = base64.standard_b64encode(img_path.read_bytes()).decode("utf-8")
# image_block = {
#     "type": "image",
#     "source": {"type": "base64", "media_type": "image/png", "data": b64},
# }

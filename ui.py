import base64
from pathlib import Path

import streamlit as st

IMAGE_DIR = Path(__file__).parent / "images"


@st.cache_data
def _encode(path_str):
    path = Path(path_str)
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def banner(title, subtitle="", image=None, emoji="📚"):
    """Full-width hero banner. Uses images/<image> if it exists, otherwise a gradient."""
    background = "linear-gradient(135deg, #1b2b23 0%, #2f4a3c 55%, #8a6d2f 100%)"

    if image and (IMAGE_DIR / image).exists():
        url = _encode(str(IMAGE_DIR / image))
        background = (
            "linear-gradient(rgba(15,25,20,0.60), rgba(15,25,20,0.78)), "
            f"url('{url}') center/cover"
        )

    html = (
        f'<div style="background:{background}; padding:2.4rem 2rem; '
        f'border-radius:14px; margin-bottom:1.2rem;">'
        f'<h1 style="color:#f1e8d4; margin:0; padding:0;">{emoji} {title}</h1>'
        f'<p style="color:#d4a64a; margin:0.4rem 0 0 0; font-size:1.05rem;">{subtitle}</p>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
# app.py - Minimal & Branded OutlineIQ
import streamlit as st
from pathlib import Path
import json
from utils import extract_outline

st.set_page_config(page_title="OutlineIQ", page_icon="📑", layout="centered")

# ------------------ Custom CSS ------------------
st.markdown(
    """
    <style>
    :root {
      --bg:#071016;
      --card:#0f1720;
      --muted:#9fb7c8;
      --accent:#1fb6ff;
    }
    .stApp { background: var(--bg); color: #eaf6ff; }

    /* Header */
    .hero { display:flex; align-items:center; gap:18px; margin-top:20px; margin-bottom:26px; }
    .logo { width:72px; height:72px; border-radius:14px; background:linear-gradient(135deg,#0f2230,#123a4a); display:flex; align-items:center; justify-content:center; font-size:32px; }
    .title { font-size:36px; font-weight:800; margin:0; color:#e9fbff; }
    .tag { color:var(--muted); margin-top:4px; }

    /* Upload card */
    .upload-box { background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.02)); border-radius:16px; padding:26px; border:1px solid rgba(255,255,255,0.05); box-shadow: 0 16px 40px rgba(2,6,23,0.6); width: 800px; max-width: calc(100% - 40px); margin: 0 auto; }
    .stFileUploader > div { padding:20px !important; border-radius:12px; background:rgba(255,255,255,0.03); border:2px dashed rgba(255,255,255,0.08); }
    .stFileUploader button { background: linear-gradient(90deg,var(--accent),#4bd1ff) !important; border-radius:10px !important; color:#032027 !important; padding:10px 14px !important; font-weight:600; }
    .hint { text-align:center; color:var(--muted); margin-top:10px; }

    /* Results */
    .results { width:800px; max-width:calc(100%-40px); margin:30px auto; display:grid; grid-template-columns: 2fr 1fr; gap:20px; }
    .card { background:var(--card); border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,0.05); }
    .small-muted { color:var(--muted); font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Header ------------------
cols = st.columns([0.15, 0.85])
with cols[0]:
    logo_path = Path("logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=72)
    else:
        st.markdown('<div class="logo">📑</div>', unsafe_allow_html=True)
with cols[1]:
    st.markdown('<div class="hero"><div><h1 class="title">OutlineIQ</h1><p class="tag">Extract structured outlines, links, and images from PDFs.</p></div></div>', unsafe_allow_html=True)

# ------------------ Upload ------------------
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Main flow ------------------
if uploaded_file:
    with st.spinner("🔎 Extracting..."):
        try:
            title, headings, metadata = extract_outline(uploaded_file.read())
            result = {"title": title, "headings": headings, "metadata": metadata}
        except Exception as e:
            st.error(f"❌ Extraction failed: {e}")
            result = None

    if result:
        st.success("✅ Extraction complete!")

        # Show document title
        st.markdown(f"<h3>{result['title']}</h3>", unsafe_allow_html=True)

        # Results grid
        st.markdown('<div class="results">', unsafe_allow_html=True)

        # Outline card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📘 Outline")
        if result["headings"]:
            table_html = "<table style='width:100%;border-collapse:collapse'>"
            table_html += "<tr><th align='left'>Level</th><th align='left'>Text</th><th>Page</th></tr>"
            for h in result["headings"]:
                lvl = h.get("level", "")
                color = "#1fb6ff" if lvl == "H1" else ("#ffb547" if lvl == "H2" else "#ffd166")
                table_html += f"<tr><td><span style='background:{color};padding:4px 8px;border-radius:6px;color:#0a0a0a;font-weight:700'>{lvl}</span></td><td>{h.get('text')}</td><td align='center'>{h.get('page')}</td></tr>"
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.write("No headings detected.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Links card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔗 Links")
        if result["metadata"]["links"]:
            for link in result["metadata"]["links"]:
                st.markdown(f"- [Page {link['page']}] <a href='{link['uri']}' target='_blank' style='color:#9fe0ff'>{link['uri']}</a>", unsafe_allow_html=True)
        else:
            st.write("No links found.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Images
        st.subheader("🖼 Image Previews")
        images = result["metadata"].get("image_previews", [])
        if images:
            cols = st.columns(4)
            for i, img in enumerate(images):
                with cols[i % 4]:
                    st.image(img["preview"], caption=f"Page {img['page']}", use_column_width=True)
        else:
            st.write("No images detected.")

        # Download JSON
        json_blob = json.dumps(result, indent=2, ensure_ascii=False)
        st.download_button("⬇️ Download JSON", data=json_blob, file_name=f"{Path(uploaded_file.name).stem}_outline.json", mime="application/json", use_container_width=True)
else:
    st.markdown("<div class='hint'>📂 Upload a PDF to get started</div>", unsafe_allow_html=True)

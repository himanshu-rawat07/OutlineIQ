# OutlineIQ

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://himanshu-rawat07-outlineiq.streamlit.app/)

**OutlineIQ** is a sleek PDF-to-JSON web tool powered by Streamlit. It intelligently extracts structured outlines, hyperlinks, and image previews from your PDFs — all in a clean, interactive interface.

---

## 🚀 Live Demo

Experience it live here: **[https://himanshu-rawat07-outlineiq.streamlit.app/](https://himanshu-rawat07-outlineiq.streamlit.app/)**

---

## ✨ Features

- 📘 **Upload PDFs** via browser — no installation required.
- 📝 **Extract headings** (H1/H2/H3) with page numbers and font-size detection.
- 🔗 **Detect hyperlinks** and list them by page.
- 🖼 **Preview embedded images** as thumbnails.
- 📤 **Download a clean JSON** file with title, outline, links, and images.
- 🎨 **Modern, branded UI** with clear action flow.

---

## 📖 Usage

1. Click the badge above to open the app.
2. Upload any PDF file.
3. Wait briefly — the app will process and show the outline, links, and images.
4. Download the structured JSON with one click.

---

## 💻 Run Locally

```bash
git clone https://github.com/himanshu-rawat07/OutlineIQ.git
cd OutlineIQ

python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

pip install -r requirements.txt
streamlit run app.py
```

---

## 🐳 Docker (Batch Conversion)

Convert multiple PDFs in one go:

1. **Build Docker image:**
   ```bash
   docker build -t outlineiq .
   ```

2. **Run batch processing:**
   ```bash
   docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" outlineiq
   ```

---

## 📂 Project Structure

```
OutlineIQ/
├── app.py
├── main.py
├── utils.py
├── Dockerfile
├── requirements.txt
├── README.md
├── input/        ← Put PDFs here
├── output/       ← JSON output directory
└── logo.png (optional)
```

---

## 🌐 Deployment Info

- Hosted on **Streamlit Community Cloud**
- Automatically builds on every GitHub push
- Uses clean layout and styling for a polished user experience

---

## 👨‍💻 Author

Made with ❤️ by **Himanshu Singh Rawat**, powered by Streamlit & PyMuPDF.

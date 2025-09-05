# 📑 OutlineIQ

**OutlineIQ** is a smart PDF processing tool that extracts structured outlines (headings), hyperlinks, and images from PDF files.  
It provides two modes:

- 🎨 **UI Mode** — Streamlit web app for interactive use.  
- ⚡ **Batch Mode** — process multiple PDFs automatically (via `main.py` or Docker).  

---

## ✨ Features
- 📘 Extract PDF **title** and hierarchical **headings** (H1/H2/H3).  
- 🔗 Detect and list **hyperlinks** with page numbers.  
- 🖼 Extract **images** and generate **thumbnail previews**.  
- 📥 Export clean **JSON** output.  
- 🎨 **Streamlit UI** with upload, preview, and download options.  
- 🐳 **Docker support** for both UI and batch mode.  

---

## 📂 Project Structure
```
OutlineIQ/
├── app.py            # Streamlit UI (frontend)
├── main.py           # Batch processor
├── utils.py          # Extraction logic
├── requirements.txt  # Dependencies
├── Dockerfile        # Build container for UI/batch
├── input/            # Place PDFs here (batch mode)
├── output/           # JSON output (batch mode)
└── README.md
```

---

## 🚀 Getting Started

### ▶️ Run Locally (UI Mode)
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser at [http://localhost:8501](http://localhost:8501).

---

### ⚡ Run Locally (Batch Mode)
1. Place your PDFs inside the `input/` folder.  
2. Run:
   ```bash
   python main.py
   ```
3. Extracted JSON files will appear inside the `output/` folder.

---

### 🐳 Run with Docker

#### Build Image
```bash
docker build -t outlineiq .
```

#### Batch Mode (default)
Processes all PDFs from `input/` → `output/`:
```bash
docker run --rm   -v "$(pwd)/input:/app/input"   -v "$(pwd)/output:/app/output"   outlineiq
```

#### UI Mode (Streamlit)
Launches the web app at [http://localhost:8501](http://localhost:8501):
```bash
docker run --rm -p 8501:8501   -v "$(pwd)/input:/app/input"   -v "$(pwd)/output:/app/output"   outlineiq streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

---

## 📂 Sample JSON Output
```json
{
  "title": "Example PDF",
  "headings": [
    {"level": "H1", "text": "Introduction", "page": 1, "font_size": 20.5},
    {"level": "H2", "text": "Overview", "page": 2, "font_size": 16.3}
  ],
  "metadata": {
    "pages_with_images": [3],
    "links": [{"page": 2, "uri": "https://example.com"}],
    "image_previews": [{"page": 3, "preview": "data:image/png;base64,..."}]
  }
}
```

---

## 👨‍💻 Author
Made with ❤️ by **Himanshu Singh Rawat**

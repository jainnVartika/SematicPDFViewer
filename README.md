# Adobe_hackathon
# 🧠 Sematic PDF Viewer

## 📌 Problem Statement

This project is built for **Round 1A: Understand Your Document** of the Adobe Hackathon 2025. The goal is to extract a clean, structured outline from a PDF, including:

- **Document Title**
- **Headings**: H1, H2, and H3
- **Page numbers**
- **Section type**: e.g., Abstract, Introduction, Conclusion (if detectable)

This outline forms the semantic foundation for later rounds.

---

## 🛠️ Approach

### ✨ Strategy
- The extractor uses **pdfplumber** to read individual characters and lines.
- Font size frequencies are used to **dynamically assign H1, H2, and H3** heading levels (not hardcoded).
- The output is sorted hierarchically using heading levels and page numbers.
- A lightweight rules-based classifier detects **section types** such as "abstract", "introduction", etc.

### ✅ Key Features
- Title detection from the largest font.
- Hierarchical heading structure using most frequent font sizes.
- Handles noisy formatting with custom filters.
- Works fully offline with no internet or external models.

---

## 🗂️ Directory Structure
├── input/
│ └── sample.pdf
├── output/
│ └── sample_output.json
├── parser.py
├── requirements.txt
├── Dockerfile
└── README.md

---

## 🐳 Docker Setup

This project runs entirely in a Docker container.

### 🔧 Build Docker Image
```bash
docker build --platform linux/amd64 -t insightpdf-extractor:vartika19 .

🚀 Run the Container
bash
docker run --rm \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  --network none \
  insightpdf-extractor:vartika19

📥 Input Format
All PDFs should be placed inside the input/ folder.

Example:

bash
input/sample.pdf

📤 Output Format
The script will generate a corresponding .json for every .pdf in input/.

Example:

json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1, "section_type": "introduction" },
    { "level": "H2", "text": "What is AI?", "page": 2, "section_type": "other" },
    { "level": "H3", "text": "History of AI", "page": 3, "section_type": "other" }
  ]
}

📚 Dependencies
These are installed from requirements.txt:
pdfplumber

🧪 Notes
Tested with both simple and complex PDFs.

Currently handles English documents.

No GPU or internet required.

🤖 Author
Vartika Jain and Sneha Sahu
Adobe Hackathon 2025 – Round 1A Submission
Project: Sematic PDF Viewer - Smart Outline · Seamless Navigation · Get to the Core · Fast
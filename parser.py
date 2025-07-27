import os
import pdfplumber
import json
import re
from collections import defaultdict, Counter


def clean_heading(text):
    return re.sub(r"(?<=\d)([A-Z])", r" \1", text)

def label_section(text):
    lowered = text.lower()
    if "abstract" in lowered:
        return "abstract"
    elif "introduction" in lowered:
        return "introduction"
    elif "method" in lowered:
        return "method"
    elif "result" in lowered or "discussion" in lowered:
        return "results"
    elif "conclusion" in lowered:
        return "conclusion"
    elif "related" in lowered:
        return "related work"
    elif "reference" in lowered:
        return "references"
    else:
        return "other"

def extract_outline(pdf_path):
    outline = []
    font_sizes = set()
    all_lines = []
    possible_titles = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            line_map = defaultdict(list)

            for char in page.chars:
                try:
                    size = round(char["size"], 1)
                    text = char["text"].strip()
                    top = round(char["top"])
                    x0 = char["x0"]

                    if not text or text in [".", ",", "-", "’", "'", "”", "“"]:
                        continue

                    key = (top, size)
                    line_map[key].append((x0, text, size))
                    font_sizes.add(size)
                except KeyError:
                    continue

            for (top, font_size), char_list in line_map.items():
                sorted_chars = sorted(char_list, key=lambda x: x[0])
                full_text = ''.join([ch[1] for ch in sorted_chars]).strip()
                full_text = clean_heading(full_text)

                if len(full_text) < 3:
                    continue

                if i < 2:  # First two pages are best place to look for title
                    possible_titles.append((font_size, full_text))

                all_lines.append((font_size, full_text, i+1))

    # Detect title (largest font from early pages)
    if possible_titles:
        title = max(possible_titles, key=lambda x: x[0])[1]
    else:
        title = ""

    # Detect H1, H2, H3 font sizes
    font_size_counter = Counter([fs for fs, _, _ in all_lines])
    most_common = font_size_counter.most_common()

    if len(most_common) >= 3:
        h1_size, h2_size, h3_size = [item[0] for item in most_common[:3]]
    elif len(most_common) == 2:
        h1_size, h2_size = [item[0] for item in most_common[:2]]
        h3_size = min(font_sizes)
    else:
        h1_size = max(font_sizes)
        h2_size = h3_size = min(font_sizes)

    heading_font_sizes = {h1_size, h2_size, h3_size}
    for font_size, text, page_num in all_lines:
      if font_size in heading_font_sizes or any(k in text.lower() for k in ["abstract", "introduction", "conclusion", "method", "results", "discussion", "references"]):
        if font_size == h1_size:
            level = "H1"
            if not title:
                title = text
        elif font_size == h2_size:
            level = "H2"
        elif font_size == h3_size:
            level = "H3"
        else:
            level = "H3"  # default fallback

        outline.append({
            "level": level,
            "text": text,
            "page": page_num,
            "section_type": label_section(text)
        })


      

    level_order = {"H1": 1, "H2": 2, "H3": 3}
    outline.sort(key=lambda x: (x["page"], level_order.get(x["level"], 4)))

    return {
        "title": title,
        "outline": outline
    }
if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_pdf = os.path.join(input_dir, filename)
            output_json = os.path.join(output_dir, filename.replace(".pdf", ".json"))

            print(f"\n📥 Reading file: {input_pdf}")
            result = extract_outline(input_pdf)

            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            print(f"✅ Saved: {output_json}")

import pymupdf
from config import *
import json

pdf_path = "D:\\AI Books\\Deep Learning.pdf"

doc = pymupdf.open(pdf_path)
pages = [doc.load_page(i) for i in range(doc.page_count)]

content_pages = pages[15:737]

toc = doc.get_toc()

useless_titles = ["bibliography", "index", "contents", "acknowledgments", "website"]

new_toc = []

for item in toc:
    title = item[1].lower().strip()
    if title not in useless_titles:
        new_toc.append(item)

toc = new_toc


def chunk_text(extracted_pages, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    words = []
    word_pages = []
    chunks = []
    start = 0
    chunk_id = 0
    for page_num, text in extracted_pages:
        page_words = text.split()
        words.extend(page_words)
        word_pages.extend([page_num] * len(page_words))
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunk_page = word_pages[start:end]
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk,
            "page_start": min(chunk_page),
            "page_end": max(chunk_page),
            "chapter": "Unknown"
        })
        chunk_id += 1
        start += chunk_size - chunk_overlap
    return chunks



extracted_pages = [(i + 15, page.get_text()) for i, page in enumerate(content_pages)]

chunked_text = chunk_text(extracted_pages)

def chapter_mapping(toc, page_num):
    chapter = "Unknown"
    for item in toc:
        if item[2] <= page_num:
            chapter = item[1]
        else:
            break
    return chapter

toc_sorted = sorted(toc, key=lambda x: x[2])

for chunk in chunked_text:
    chunk["chapter"] = chapter_mapping(toc_sorted, chunk["page_start"])

toc_json = json.dumps(toc_sorted, indent=2)
with open("data/toc.json", "w", encoding="utf-8") as f:
    f.write(toc_json)
chunks_json = json.dumps(chunked_text, indent=2)
with open("data/chunks.json", "w", encoding="utf-8") as f:
    f.write(chunks_json)


print(toc)
import re
import lancedb
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
cleaned_dir = Path(r"C:\Users\Temporary\Documents\RAGProject\CleanedData")
db_path = r"C:\Users\Temporary\Documents\RAGProject\VectorDB"

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")

# Connect to LanceDB and create table
db = lancedb.connect(db_path)

# Headings to skip for class reference files
SKIP_SECTIONS = {"Properties", "Methods", "Tutorials"}

def get_page_title(content):
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Unknown"

def is_class_file(filename):
    return filename.startswith("class_")

def split_into_chunks(content, filename):
    chunks = []
    title = get_page_title(content)
    class_file = is_class_file(filename)

    # Determine heading pattern based on file type
    if class_file:
        heading_pattern = re.compile(r'^## (.+)$', re.MULTILINE)
    else:
        heading_pattern = re.compile(r'^#{2,3} (.+)$', re.MULTILINE)

    # Find all heading positions
    matches = list(heading_pattern.finditer(content))

    if not matches:
        # No headings found, treat entire file as one chunk
        chunks.append({
            "text": content.strip(),
            "title": title,
            "section": "Overview",
            "source": filename
        })
        return chunks

    # Add content before first heading as an intro chunk
    intro = content[:matches[0].start()].strip()
    if intro:
        chunks.append({
            "text": intro,
            "title": title,
            "section": "Overview",
            "source": filename
        })

    # Process each section
    for i, match in enumerate(matches):
        section_name = match.group(1).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_content = content[start:end].strip()

        # Skip summary table sections in class reference files
        if class_file and section_name in SKIP_SECTIONS:
            continue

        # For class reference files, further split on --- separators
        if class_file:
            entries = re.split(r'\n---\n', section_content)
            for entry in entries:
                entry = entry.strip()
                if entry:
                    chunks.append({
                        "text": entry,
                        "title": title,
                        "section": section_name,
                        "source": filename
                    })
        else:
            chunks.append({
                "text": section_content,
                "title": title,
                "section": section_name,
                "source": filename
            })

    return chunks

# Collect all chunks from all files
print("Chunking markdown files...")
all_chunks = []
md_files = list(cleaned_dir.rglob("*.md"))
total = len(md_files)

for i, md_file in enumerate(md_files, start=1):
    content = md_file.read_text(encoding="utf-8", errors="ignore")
    chunks = split_into_chunks(content, md_file.name)
    all_chunks.extend(chunks)
    print(f"Chunked {i} of {total}: {md_file.name} ({len(chunks)} chunks)")

print(f"\nTotal chunks: {len(all_chunks)}")

# Embed all chunks
print("\nEmbedding chunks...")
texts = [chunk["text"] for chunk in all_chunks]
embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

# Build records for LanceDB
print("\nWriting to LanceDB...")
records = []
for chunk, embedding in zip(all_chunks, embeddings):
    records.append({
        "vector": embedding.tolist(),
        "text": chunk["text"],
        "title": chunk["title"],
        "section": chunk["section"],
        "source": chunk["source"]
    })

# Write to database
table = db.create_table("godot_docs", data=records, mode="overwrite")
print(f"\nDone! {len(records)} chunks written to VectorDB.")
import pickle
import sys
from pathlib import Path

from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter

PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else "guida_python.pdf"
OUT_PATH = Path("chunks.pkl")

converter = DocumentConverter()
result = converter.convert(PDF_PATH)
markdown = result.document.export_to_markdown()

headers_to_split_on = [
    ("#", "titolo"),
    ("##", "sezione"),
    ("###", "sottosezione"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(markdown)

with OUT_PATH.open("wb") as f:
    pickle.dump(chunks, f)

print(f"Chunk generati: {len(chunks)}")
for chunk in chunks[:2]:
    print(f"  Metadata: {chunk.metadata}")
    print(f"  Testo:    {chunk.page_content[:120]}...")
    print()
print(f"\nSalvati in {OUT_PATH}")

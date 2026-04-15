from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter

# 1. Estrai il documento sorgente in markdown strutturato con docling
converter = DocumentConverter()
result = converter.convert("manuale.pdf")
markdown = result.document.export_to_markdown()

# 2. Definisci quali livelli di header diventano metadata
headers_to_split_on = [
    ("#", "titolo"),
    ("##", "sezione"),
    ("###", "sottosezione"),
]

# 3. Chunka per header: ogni chunk porta con sé la sua posizione nel documento
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(markdown)

for chunk in chunks[:3]:
    print("Metadata:", chunk.metadata)
    print("Contenuto:", chunk.page_content[:200])
    print("---")
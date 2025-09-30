import io
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient, IndexDocumentsBatch
from pdfminer.high_level import extract_text as pdf_to_text
from docx import Document
from bs4 import BeautifulSoup
from app.chunker import chunk_text
from app.llm import embed_text
from app.ocr import extract_text_from_image
from app.config import settings

cred = DefaultAzureCredential()
blob = BlobServiceClient(account_url=settings.blob_account_url, credential=cred)
search = SearchClient(settings.search_endpoint, settings.search_index, credential=cred)

def parse_pdf(data: bytes) -> str:
    return pdf_to_text(io.BytesIO(data))

def parse_docx(data: bytes) -> str:
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs)

def parse_html(data: bytes) -> str:
    soup = BeautifulSoup(data, "html.parser")
    return soup.get_text(separator="\n")

def process_blob(name: str, data: bytes, metadata: dict):
    if name.endswith(".pdf"):
        text = parse_pdf(data)
    elif name.endswith(".docx"):
        text = parse_docx(data)
    elif name.endswith(".html") or name.endswith(".htm"):
        text = parse_html(data)
    elif any(name.endswith(x) for x in [".png", ".jpg", ".jpeg", ".tif"]):
        text = extract_text_from_image(data)
    else:
        print(f"Unsupported file: {name}")
        return

    if not text.strip():
        print(f"No text extracted from: {name}")
        return

    chunks = chunk_text(text, target_tokens=1000, overlap=150)
    vectors = [embed_text(c) for c in chunks]

    batch = IndexDocumentsBatch()
    now = datetime.utcnow().isoformat() + "Z"
    for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
        doc = {
            "id": f"{name}-{i}",
            "content": chunk,
            "contentVector": vec,
            "sourcePath": name,
            "pageStart": metadata.get("pageStart", 0),
            "pageEnd": metadata.get("pageEnd", 0),
            "section": metadata.get("section", ""),
            "doctype": metadata.get("doctype", ""),
            "product": metadata.get("product", ""),
            "version": metadata.get("version", ""),
            "lastModified": now,
        }
        batch.add_upload_action(doc)
    search.index_documents(batch)
    print(f"Ingested {len(chunks)} chunks from {name}")

def ingest_all_blobs():
    container = blob.get_container_client(settings.blob_container)
    for b in container.list_blobs():
        data = container.download_blob(b.name).readall()
        metadata = b.metadata or {}
        process_blob(b.name, data, metadata)

if __name__ == "__main__":
    ingest_all_blobs()

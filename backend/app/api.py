from fastapi import APIRouter, UploadFile, File, Form
from app.llm import ask_llm, embed_text
from app.ocr import extract_text_from_image
from app.retriever import retrieve_context

router = APIRouter()

@router.post("/chat")
async def chat(
    message: str = Form(...),
    product: str | None = Form(None),
    version: str | None = Form(None),
    file: UploadFile | None = File(None),
    top_k: int = Form(8)
):
    """Main chat endpoint: combines OCR, retrieval, and LLM."""
    ocr_text = ""
    if file:
        content = await file.read()
        ocr_text = extract_text_from_image(content)

    query = message if not ocr_text else f"{message}\n\n[From OCR]\n{ocr_text}"
    vector = embed_text(query)
    snippets = retrieve_context(query, vector, product, version, top_k)

    if not snippets:
        return {"answer": "I don’t know based on the available SAS documents.", "citations": []}

    context = "\n\n".join(snippets)
    answer = ask_llm(query, context)

    if "I don’t know" in answer:
        return {"answer": "I don’t know based on the available SAS documents.", "citations": []}

    citations = [s.split("(", 1)[1].split(")")[0] for s in snippets[:3]]

    return {"answer": answer, "citations": citations}

def chunk_text(text: str, target_tokens: int = 1000, overlap: int = 150) -> list[str]:
    """Split text into overlapping chunks for embedding and indexing."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + target_tokens, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

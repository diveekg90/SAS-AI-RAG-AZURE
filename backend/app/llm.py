from openai import AzureOpenAI
from app.config import settings

client = AzureOpenAI(
    azure_endpoint=settings.aoai_endpoint,
    api_key=settings.aoai_key,
    api_version=settings.aoai_api_version,
)

def ask_llm(query: str, context: str) -> str:
    """Send query + context to Azure OpenAI chat deployment."""
    messages = [
        {"role": "system", "content": (
            "You are a SAS assistant. Only answer from the provided context. "
            "If unsure, reply: I don’t know based on the available SAS documents."
        )},
        {"role": "user", "content": f"Question:\n{query}\n\nContext:\n{context}"}
    ]
    resp = client.chat.completions.create(
        model=settings.aoai_chat_deployment,
        messages=messages,
        temperature=0.1,
        max_tokens=700,
    )
    return resp.choices[0].message.content.strip()

def embed_text(text: str) -> list[float]:
    """Generate embeddings from Azure OpenAI embed deployment."""
    resp = client.embeddings.create(
        input=[text],
        model=settings.aoai_embed_deployment
    )
    return resp.data[0].embedding

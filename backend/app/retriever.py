from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from app.config import settings

search_client = SearchClient(
    endpoint=settings.search_endpoint,
    index_name=settings.search_index,
    credential=DefaultAzureCredential()
)

def retrieve_context(query: str, vector: list[float], product: str | None = None, version: str | None = None, top_k: int = 8) -> list[str]:
    """Perform hybrid retrieval from Azure Cognitive Search."""
    filters = []
    if product:
        filters.append(f"product eq '{product}'")
    if version:
        filters.append(f"version eq '{version}'")
    filter_expr = " and ".join(filters) if filters else None

    results = search_client.search(
        search_text=query,
        vectors=[{"value": vector, "fields": "contentVector", "k": 20}],
        filter=filter_expr,
        select=["content", "sourcePath", "pageStart", "pageEnd", "section"],
        query_type="semantic",
        semantic_configuration_name="sem",
        top=20,
    )

    snippets = []
    for i, r in enumerate(results):
        snippets.append(f"[{i+1}] ({r['sourcePath']} p.{r['pageStart']}-{r['pageEnd']}) {r['content'][:2000]}")
        if len(snippets) >= top_k:
            break
    return snippets

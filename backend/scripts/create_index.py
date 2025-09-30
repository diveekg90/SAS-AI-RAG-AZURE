from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField, VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile
from app.config import settings

def create_index():
    client = SearchIndexClient(endpoint=settings.search_endpoint, credential=AzureKeyCredential(settings.aoai_key))
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="content", type="Edm.String"),
        SimpleField(name="contentVector", type="Collection(Edm.Single)"),
        SearchableField(name="sourcePath", type="Edm.String"),
        SimpleField(name="pageStart", type="Edm.Int32"),
        SimpleField(name="pageEnd", type="Edm.Int32"),
        SearchableField(name="section", type="Edm.String"),
        SearchableField(name="doctype", type="Edm.String"),
        SearchableField(name="product", type="Edm.String"),
        SearchableField(name="version", type="Edm.String"),
    ]

    vector_search = VectorSearch(
        algorithm_configurations=[HnswAlgorithmConfiguration(name="default")],
        profiles=[VectorSearchProfile(name="default", algorithm_configuration_name="default")]
    )

    index = SearchIndex(name=settings.search_index, fields=fields, vector_search=vector_search)
    client.create_index(index)
    print(f"Index {settings.search_index} created.")

if __name__ == "__main__":
    create_index()

from typing import Annotated, Any

from pydantic import BaseModel

from semantic_kernel.connectors.ai.open_ai import OpenAIEmbeddingPromptExecutionSettings
from semantic_kernel.data import (
    VectorStoreRecordDataField,
    VectorStoreRecordKeyField,
    VectorStoreRecordVectorField,
    vectorstoremodel,
    VectorSearchOptions
)
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchCollection
from semantic_kernel.functions import kernel_function
import os

@vectorstoremodel
class DocSampleClass(BaseModel):
    id: Annotated[str, VectorStoreRecordKeyField]
    title: Annotated[str | None, VectorStoreRecordDataField()] = None
    content: Annotated[
        str,
        VectorStoreRecordDataField(
            has_embedding=True, embedding_property_name="contentVector", is_full_text_searchable=True
        ),
    ]
    contentVector: Annotated[
        list[float] | None,
        VectorStoreRecordVectorField(
            dimensions=1536,
            local_embedding=True,
            embedding_settings={"embedding": OpenAIEmbeddingPromptExecutionSettings(dimensions=1536)},
        ),
    ] = None
    url: Annotated[str | None, VectorStoreRecordDataField()] = None
    filepath: Annotated[str, VectorStoreRecordDataField()]
    meta_json_string: Annotated[str | None, VectorStoreRecordDataField()] = None

kernel = Kernel()

class SearchPlugin:
    def __init__(self):
        self.embedding_service = AzureTextEmbedding(service_id="ada-embedding-service",
                                                    deployment_name=os.getenv("EMBEDDINGS_DEPLOYMENT_NAME"),
                                                    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                                    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
                                                    )
        kernel.add_service(self.embedding_service)
        self.collection = AzureAISearchCollection[DocSampleClass](
            data_model_type=DocSampleClass, collection_name="employeehandbook", 
            search_endpoint=os.getenv("AI_SEARCH_URL"),
            api_key=os.getenv("AI_SEARCH_KEY"),
        )
        

    @kernel_function(description="Invoke azure ai search with the embeddings provided by the text embedding service")
    async def invoke_azure_aisearch(self, 
                                    query: str
        ):
        if not await self.collection.does_collection_exist():
            raise ValueError(
                "Collection does not exist, please create using the "
                "Azure AI Search portal wizard -> Import Data -> Samples -> hotels-sample."
                "During creation adopt the schema to add the description_vector and description_fr_vector fields."
                "Then run this sample with `first_run=True` to add the vectors."
            )
        
        # Search using just text, by default this will search all the searchable text fields in the index.
        # results = await self.collection.text_search(search_text=query)
        # print("Search results using text: ")
        # async for result in results.results:
        #     print(
        #         f"{result.record.id} (in {result.record.content}): (score: {result.score})"
        #     )

        # print("\n")

        # Generate the vector for the query
        query_vector = (await self.embedding_service.generate_raw_embeddings([query]))[0]
        # print("Search results using vector: ")
        # Use vectorized search to search using the vector.
        results = await self.collection.vectorized_search(
            vector=query_vector,
            options=VectorSearchOptions(vector_field_name="contentVector"),
        )
        async for result in results.results:
            return result.record
        
        return ""
        

        
    def __del__(self):
        # Delete the collection object so that the connection is closed.
        try:
           del self.collection
        except Exception as e:
            print(e)

if __name__ == "__main__":
    from dotenv import load_dotenv
    import asyncio
    load_dotenv()
    
    query = "what are important policies?"
    search_plugin_obj = SearchPlugin()
    asyncio.run(search_plugin_obj.invoke_azure_aisearch(query=query))

    
    
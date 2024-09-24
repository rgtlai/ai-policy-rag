from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os
load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings_ft = HuggingFaceEmbeddings(model_name="rgtlai/ai-policy-ft")

client = QdrantClient(
    api_key=os.environ["QDRANT_API_KEY"],
    url=os.environ["QDRANT_URI"]
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name=os.environ["QDRANT_COLLECTION"],
    embedding=embeddings,
)

vector_store_ft = QdrantVectorStore(
    client=client,
    collection_name=os.environ["QDRANT_COLLECTION_FT"],
    embedding=embeddings_ft,
)

vector_store_ft_500 = QdrantVectorStore(
    client=client,
    collection_name=os.environ["QDRANT_COLLECTION_FT_500"],
    embedding=embeddings_ft,
)

retriever = vector_store.as_retriever()
retriever_ft = vector_store_ft.as_retriever()
retriever_ft_500 = vector_store_ft_500.as_retriever()

if __name__ == '__main__':
    query = "What is NIST document about?"
    results = retriever.invoke(query)
    print('****', results)
    results = retriever_ft.invoke(query)
    print('****FT', results)
    results = retriever_ft_500.invoke(query)
    print('****FT_500', results)


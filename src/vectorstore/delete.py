from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
load_dotenv()

client = QdrantClient(
    api_key=os.environ["QDRANT_API_KEY"],
    url=os.environ["QDRANT_URI"]
)

client.delete_collection(collection_name=os.environ["QDRANT_COLLECTION"])
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = QdrantClient("localhost", port=6333, timeout=10)  # Added timeout
COLLECTION_NAME = "video_frames"

def initialize_db():
    try:
        # Check if collection exists before recreating
        collections = client.get_collections()
        existing = any(c.name == COLLECTION_NAME for c in collections.collections)
        
        if existing:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists")
        else:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=512, distance=Distance.COSINE)
            )
            logger.info(f"✅ Created new collection '{COLLECTION_NAME}'")
            
    except Exception as e:
        logger.error(f"❌ Error initializing database: {str(e)}")
        raise

def store_vector(frame_id: int, vector: list, frame_path: str):
    try:
        if len(vector) != 512:
            logger.warning(f"⚠️ Frame {frame_id} vector has {len(vector)} dimensions (expected 512)")
            return

        # Upsert point with integer ID
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[PointStruct(
                id=frame_id,
                vector=vector,
                payload={"path": frame_path}
            )]
        )
        logger.info(f"💾 Stored vector for frame {frame_id}")
        
    except Exception as e:
        logger.error(f"❌ Error storing vector for frame {frame_id}: {str(e)}")

def search_similar(vector: list, limit: int = 5):
    try:
        logger.info(f"Searching with vector sample: {vector[:5]}...")
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            with_vector=True
        )
        logger.info(f"🔍 Found {len(results)} matches")
        return results
    except Exception as e:
        logger.error(f"❌ Search failed: {str(e)}")
        return []

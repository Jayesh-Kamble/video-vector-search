from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uuid
import os
from . import video_processor
from . import feature_db
from .schemas import FeatureVector
import math
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Video Vector Search API", description="Upload videos and search similar frames")

# Initialize Qdrant collection
feature_db.initialize_db()

@app.post("/upload-video")
async def upload_video(
    file: UploadFile = File(...),
    interval: int = 1
):
    logger.info(f"Starting video upload: {file.filename}")
    
    # Validate MP4 format
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 format is supported.")

    os.makedirs("data/videos", exist_ok=True)
    os.makedirs("data/frames", exist_ok=True)

    # Save video
    video_id = str(uuid.uuid4())
    video_path = f"data/videos/{video_id}.mp4"
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
    logger.info(f"Video saved to: {video_path}")

    # Extract frames
    logger.info("Extracting frames...")
    frame_paths = video_processor.extract_frames(video_path, interval, "data/frames")
    logger.info(f"Extracted {len(frame_paths)} frames")

    # Compute and store features
    logger.info("Computing feature vectors...")
    first_frame_vector = None
    for idx, path in enumerate(frame_paths):
        vector = video_processor.compute_histogram(path)
        
        # Log full vector only for first frame to avoid clutter
        if idx == 0:
            logger.info(f"Frame {idx} vector: {vector}")
        else:
            logger.info(f"Frame {idx} vector length: {len(vector)}, sample: {vector[:5]}...")

        # Store in database
        feature_db.store_vector(idx, vector, path)

        if idx == 0:
            first_frame_vector = vector

    logger.info("Video processing complete!")
    return {
        "video_id": video_id,
        "frames": len(frame_paths),
        "first_frame_full_vector": first_frame_vector,
        "message": "Use first_frame_full_vector for /search endpoint"
    }

@app.post("/search")
async def search_similar_frames(query: FeatureVector):
    # Validate vector dimensions
    if len(query.vector) != 512:
        raise HTTPException(
            status_code=400,
            detail=f"Vector must have 512 dimensions (got {len(query.vector)})"
        )

    # Validate vector values
    if any(math.isnan(x) or math.isinf(x) for x in query.vector):
        raise HTTPException(400, "Vector contains invalid values (NaN/inf)")

    logger.info("Searching for similar frames...")
    results = feature_db.search_similar(query.vector)
    logger.info(f"Found {len(results)} similar frames")
    
    return [
        {
            "frame_path": result.payload["path"],
            "score": result.score,
            "vector": result.vector
        } for result in results
    ]

@app.get("/get-frame/{frame_path:path}")
async def get_frame(frame_path: str):
    # Sanitize access to only data/frames folder
    base_dir = os.path.abspath("data/frames")
    requested_path = os.path.abspath(frame_path)

    if not requested_path.startswith(base_dir):
        raise HTTPException(status_code=403, detail="Access denied")

    if not os.path.exists(requested_path):
        raise HTTPException(404, "Frame not found")

    return FileResponse(requested_path)

@app.get("/")
async def root():
    return {"message": "Video Vector Search API", "docs": "/docs"}

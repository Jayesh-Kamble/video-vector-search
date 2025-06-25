# Jayesh-Kamble-video-vector-search
A FastAPI backend that allows users to upload videos, extract frames, compute color histogram feature vectors, store them in Qdrant, search for similar frames using vector similarity, and retrieve frames as images.

# 🎥 Video Vector Search API

A FastAPI backend application that enables users to:

- Upload MP4 videos  
- Extract frames at custom intervals  
- Compute 512-dimensional color histogram feature vectors  
- Store them in a **Qdrant vector database**  
- Search for visually similar frames using vector similarity  
- Retrieve frames as downloadable images  

---

## 🚀 Features

- 📤 Upload MP4 videos  
- 🖼️ Extract frames at user-defined intervals (e.g., every 1 second)  
- 🧠 Compute 512-dimensional color histogram vectors for each frame  
- 💾 Store frame vectors in Qdrant  
- 🔍 Search for similar frames using vector similarity  
- 📁 Retrieve frame images via API  

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/video-vector-search.git
cd video-vector-search
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧱 Start Qdrant (Vector DB)

Ensure Docker is installed, then run:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

## 🚦 Run the FastAPI Server

```bash
uvicorn app.main:app --reload --port 8000
```

Once running, visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 API Usage Guide

### 1. 📤 Upload a Video

- Endpoint: `POST /upload-video`  
- Upload an `.mp4` video file  
- Set your frame interval (e.g., 1 frame per second)  
- The response includes the `first_frame_full_vector` (512-dim)  

---

### 2. 🔍 Search for Similar Frames

- Endpoint: `POST /search`  
- Paste the 512-dimensional vector from the previous step  
- The API returns paths and similarity scores for matching frames  

---

### 3. 🖼️ Retrieve Frame Image

- Endpoint: `GET /get-frame/{frame_path}`  
- Use the `frame_path` value from search results to retrieve the image  

---

## 📂 Project Structure

```
video-vector-search/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── feature_db.py
│   ├── video_processor.py
│   └── schemas.py
├── data/
│   ├── videos/       # Uploaded videos
│   └── frames/       # Extracted frames
├── requirements.txt
├── README.md
└── screenshots/      # API and output screenshots
```

---

## 🧰 Troubleshooting

- ❗ **Qdrant not running:** Ensure Docker is installed and Qdrant is started before running the API.  
- 🔢 **Vector dimension mismatch:** Ensure the search vector is exactly 512 values.  
- 🕳️ **Empty search results:** Make sure upload was successful and vectors were stored (check logs).  
- 🧾 **422 JSON errors:** Use valid raw JSON for vector input — no Python expressions or comments.  

---

## 📸 Screenshots

> Add actual images in `screenshots/` folder and reference them like this:

- Swagger UI:  
  ![Swagger UI](screenshots/swagger_ui.png)

- Upload Video:  
  ![Upload Video](screenshots/upload_video.png)

- Search Results:  
  ![Search Results](screenshots/search_results.png)

- Get Frame:  
  ![Get Frame](screenshots/get_frame.png)

---

## 👤 Author

**Your Name**  
📧 your.email@example.com

---

## 📝 License

This project is for educational and demonstration purposes only.

---

Enjoy using the **Video Vector Search API**! 🚀

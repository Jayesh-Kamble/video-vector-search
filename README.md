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
git clone https://github.com/Jayesh-Kamble/video-vector-search.git
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

## A) BY using 🧱 Start Qdrant (Vector DB)

Ensure Docker is installed, then run:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

## B) Using the Qdrant Binary (No Docker)

If you downloaded Qdrant as a binary (for example, `qdrant.exe` on Windows or `qdrant` on Linux/Mac), you can run it directly:

1. **Download the Qdrant binary** for your OS from the [official Qdrant releases page](https://github.com/qdrant/qdrant/releases).
2. **Extract the binary** if needed.
3. **Open a terminal/command prompt** in the folder containing the binary.
4. **Run Qdrant:**
   - On Windows:
     ```
     qdrant.exe
     ```
   - On Linux/Mac:
     ```
     ./qdrant
     ```
5. Qdrant will start on port 6333 by default.  
   You should see a message like:  
   `Qdrant HTTP listening on 6333`

**Make sure Qdrant is running before starting your FastAPI server!**

**You only need to use one of these methods.**  
Both will make Qdrant available at `http://localhost:6333` for this project.

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

- Swagger UI:  
  ![Image](https://github.com/user-attachments/assets/16af8abe-b30e-49ee-b624-3848d48f85ad)

- Upload Video:  
  ![Image](https://github.com/user-attachments/assets/cfbab168-cf37-42cd-9f42-b50c77757e1d)

- Search Results:  
  ![Image](https://github.com/user-attachments/assets/2071397f-2c0f-42e7-8b0d-ef3769789b4b)

- Get Frame:  
![Image](https://github.com/user-attachments/assets/64d5de91-9098-4638-baa6-daa606fc4eed)

---

## 👤 Author

**Jayesh Kamble**  
📧jayeshavkamble@gmail.com

---

## 📝 License

This project is for educational and demonstration purposes only.

---

Enjoy using the **Video Vector Search API**! 🚀

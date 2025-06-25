import cv2
import numpy as np
from pathlib import Path

def extract_frames(video_path: str, interval: int, output_dir: str):
    cap = cv2.VideoCapture(video_path)
    frame_paths = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:
            frame_path = Path(output_dir) / f"frame_{frame_count}.jpg"
            cv2.imwrite(str(frame_path), frame)
            frame_paths.append(str(frame_path))
        frame_count += 1
    cap.release()
    return frame_paths

def compute_histogram(frame_path: str, bins: int = 8) -> list:
    image = cv2.imread(frame_path)
    if image is None:
        raise ValueError(f"Could not load image: {frame_path}")
    hist = cv2.calcHist([image], [0, 1, 2], None, [bins]*3, [0, 256]*3)
    return cv2.normalize(hist, hist).flatten().tolist()

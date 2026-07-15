"""
video_processor.py — Extract key frames from video using scene-change detection
and face detection.
"""

import base64
import os
import tempfile

import cv2
import numpy as np
from PIL import Image


def _has_face(frame_bgr: np.ndarray) -> bool:
    """Detect whether a frame contains a face using OpenCV's Haar Cascade."""
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return len(faces) > 0


def _frame_to_base64_jpeg(frame_bgr: np.ndarray) -> str:
    """Encode a BGR frame as a base64 JPEG string."""
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)

    # Resize to keep size manageable for LLM context
    h, w = pil_img.size
    max_dim = 512
    if max(h, w) > max_dim:
        ratio = max_dim / max(h, w)
        pil_img = pil_img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        pil_img.save(tmp.name, format="JPEG", quality=85)
        with open(tmp.name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        os.unlink(tmp.name)

    return b64


def extract_key_frames(
    video_path: str,
    max_frames: int = 4,
    prefer_faces: bool = True,
    scene_threshold: float = 30.0,
) -> list:
    """
    Extract representative key frames from a video.

    Uses histogram-based scene-change detection to pick diverse frames.
    Optionally boosts frames that contain faces.

    Args:
        video_path: Path to the video file.
        max_frames: Maximum number of key frames to return.
        prefer_faces: If True, boost frames containing faces.
        scene_threshold: Histogram difference threshold for a "new" scene.

    Returns:
        list of dicts with keys:
            - timestamp_sec (float): Timestamp in seconds.
            - has_face (bool): Whether the frame contains a face.
            - base64_jpeg (str): Base64-encoded JPEG image.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0 or total_frames <= 0:
        cap.release()
        return []

    candidates = []
    prev_hist = None
    frame_idx = 0
    sample_interval = max(1, total_frames // (max_frames * 5))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        # Only process every Nth frame for efficiency
        if frame_idx % sample_interval != 0 and frame_idx != 1:
            continue

        # Compute HSV histogram for scene-change detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

        scene_score = 0.0
        if prev_hist is not None:
            scene_score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR)
            scene_score = min(scene_score, 10.0)
        prev_hist = hist

        has_face = _has_face(frame)

        # Composite score: scene-change + face bonus
        score = scene_score
        if prefer_faces and has_face:
            score += 2.0

        timestamp = frame_idx / fps
        candidates.append({
            "timestamp_sec": round(timestamp, 2),
            "has_face": has_face,
            "score": score,
            "frame": frame,
        })

    cap.release()

    if not candidates:
        return []

    # Sort by score descending, pick top max_frames
    candidates.sort(key=lambda c: c["score"], reverse=True)
    selected = candidates[:max_frames]

    # Re-sort by timestamp for natural order
    selected.sort(key=lambda c: c["timestamp_sec"])

    results = []
    for c in selected:
        results.append({
            "timestamp_sec": c["timestamp_sec"],
            "has_face": c["has_face"],
            "base64_jpeg": _frame_to_base64_jpeg(c["frame"]),
        })

    return results
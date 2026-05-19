
import cv2
from messages import SENTINEL


class Streamer:
    def __init__(self, video_path):
        self.video_path = video_path

    def run(self, output_queue):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error: failed to open video: {self.video_path}")
            output_queue.put(SENTINEL)
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            output_queue.put(frame)

        output_queue.put(SENTINEL)
        cap.release()

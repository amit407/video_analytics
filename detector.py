
import cv2
from messages import Detection, SENTINEL


class MotionDetector:
    def __init__(self, min_area: int = 500):
        self.min_area = min_area
        self.prev_frame = None

    def detect(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_frame is None:
            self.prev_frame = gray_frame
            return []

        diff = cv2.absdiff(gray_frame, self.prev_frame)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) == 2:
            contours = cnts[0]
        else:
            contours = cnts[1]
        self.prev_frame = gray_frame
        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            detections.append(Detection(x=x, y=y, w=w, h=h))
        return detections

    def run(self, input_queue, output_queue):
        while True:
            frame = input_queue.get()

            if frame is SENTINEL:
                output_queue.put(SENTINEL)
                break

            detections = self.detect(frame)
            output_queue.put((frame, detections))

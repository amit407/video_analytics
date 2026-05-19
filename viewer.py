
from datetime import datetime
import cv2
from messages import SENTINEL


class Viewer:
    def run(self, input_queue):
        while True:
            message = input_queue.get()
            if message is SENTINEL:
                break
            frame, detections = message
            self.blur_detections(frame, detections)
            self.draw_detections(frame, detections)
            self.draw_timestamp(frame)
            cv2.imshow("Video Analytics Pipeline", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()

    def draw_detections(self, frame, detections):
        for detection in detections:
            cv2.rectangle(frame, (detection.x, detection.y), (detection.x + detection.w,detection.y + detection.h),
                          (0, 255, 0), 2)

    def draw_timestamp(self, frame):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    def blur_detections(self, frame, detections):
        for detection in detections:
            x, y, w, h = detection.x, detection.y, detection.w, detection.h
            roi = frame[y:y + h, x:x + w]
            if roi.size == 0:
                continue
            blurred_roi = cv2.GaussianBlur(roi, (29, 29), 0)
            frame[y:y + h, x:x + w] = blurred_roi

import queue
import threading
import time

import cv2

from config import DETECTED_SCREEN_NAME
from detector.detect_objects import detect_objects


class ObjectDetector:
    def __init__(self, model, frame_queue, processed_frame_queue):
        self.model = model
        self.frame_queue = frame_queue
        self.processed_frame_queue = processed_frame_queue
        self.processing = False
        self.start_time = None
        self.frame_count = 0

    def detect_objects_in_frame(self, frame):
        detected_frame, _ = detect_objects(frame, self.model)
        return detected_frame

    def process_frame(self, frame):
        detected_frame = self.detect_objects_in_frame(frame)
        self.frame_count += 1
        self.add_overlay(detected_frame)
        self.processed_frame_queue.put(detected_frame)

    def process_frames(self):
        self.processing = True
        self.start_time = time.time()

        while self.processing or not self.frame_queue.empty():
            try:
                frame = self.frame_queue.get()
                if frame is None:
                    break
                self.process_frame(frame)
            except queue.Empty:
                # print("Queue is empty, waiting for frames...")
                continue

    def add_overlay(self, frame):
        elapsed_time = time.time() - self.start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        overlay_text_time = f"Time: {formatted_time}"
        overlay_text_fps = f"FPS: {fps:.2f}"

        text_size_time = cv2.getTextSize(overlay_text_time, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_size_fps = cv2.getTextSize(overlay_text_fps, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        max_text_width = max(text_size_time[0], text_size_fps[0])

        cv2.rectangle(frame, (5, 5), (5 + max_text_width + 10, 5 + text_size_time[1] + text_size_fps[1] + 20),
                      (0, 0, 0), -1)
        cv2.putText(frame, overlay_text_time, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, overlay_text_fps, (10, 25 + text_size_time[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255, 255, 255), 2)

    def display_frame(self, detected_frame):
        try:
            if detected_frame is not None and detected_frame.size > 0:
                cv2.imshow(DETECTED_SCREEN_NAME, detected_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.stop_processing()
        except cv2.error as e:
            print(f"Error displaying frame: {e}")

    def start_processing(self):
        processing_thread = threading.Thread(target=self.process_frames)
        processing_thread.start()
        return processing_thread

    def stop_processing(self, processing_thread: threading.Thread = None):
        self.processing = False
        if processing_thread:
            processing_thread.join()


def display_processed_frames(processed_frame_queue):
    while True:
        frame = processed_frame_queue.get()
        if frame is None:
            break
        cv2.imshow(DETECTED_SCREEN_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()

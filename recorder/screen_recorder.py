import queue
import threading
import time

import cv2
import mss
import numpy as np

from config import VIDEO_FORMAT, RECORDER_FPS, QUEUE_MAX_SIZE


class ScreenRecorder:
    def __init__(self, output_file, region):
        self.output_file = output_file
        self.region = region
        self.recording = False
        self.frame_queue = queue.Queue(
            maxsize=QUEUE_MAX_SIZE)  ## niewiem czy to jest ok mozeliwe ze trzeba bedzie zmienic na 1024 * 1024 * 1024

    def setup_monitor(self):
        return {
            "top": int(self.region[1]),
            "left": int(self.region[0]),
            "width": int(self.region[2]),
            "height": int(self.region[3])
        }

    def setup_video_writer(self, monitor, video_format=VIDEO_FORMAT):
        fourcc = cv2.VideoWriter_fourcc(*video_format)
        return cv2.VideoWriter(self.output_file, fourcc, RECORDER_FPS, (monitor["width"], monitor["height"]))

    def capture_frame(self, sct, monitor):
        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def record_screen(self):
        monitor = self.setup_monitor()
        out = self.setup_video_writer(monitor)

        with mss.mss() as sct:
            self.recording = True
            start_time = time.time()
            while self.recording:
                frame = self.capture_frame(sct, monitor)
                try:
                    self.frame_queue.put(frame, timeout=1)
                except queue.Full:
                    print("Queue is full, dropping frame")
                    pass

                out.write(frame)

            out.release()
            cv2.destroyAllWindows()
            print(start_time - time.time())

    def start_recording(self):
        recording_thread = threading.Thread(target=self.record_screen)
        recording_thread.start()
        return recording_thread

    def stop_recording(self, recording_thread):
        self.recording = False
        recording_thread.join()
        self.frame_queue.put(None)

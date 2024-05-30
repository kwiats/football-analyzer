import cv2

from config import DETECTED_SCREEN_NAME


class ScreenProcessor:
    def __init__(self, recorder, detector):
        self.recorder = recorder
        self.detector = detector

    def display(self):
        try:
            self.start_processing()
            while True:
                frame = self.detector.processed_frame_queue.get()
                if frame is None:
                    break
                cv2.imshow(DETECTED_SCREEN_NAME, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.stop_processing()
            cv2.destroyAllWindows()

    def start_processing(self):
        self.recorder.start_recording()
        self.detector.start_processing()

    def stop_processing(self):
        self.recorder.stop_recording()
        self.detector.stop_processing()

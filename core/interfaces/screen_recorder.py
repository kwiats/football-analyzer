from abc import ABC, abstractmethod


class ScreenRecorderInterface(ABC):

    @abstractmethod
    def setup_monitor(self):
        pass

    @abstractmethod
    def setup_video_writer(self, monitor, video_format="mp4v"):
        pass

    @abstractmethod
    def capture_frame(self, sct, monitor):
        pass

    @abstractmethod
    def update_fps(self, fps, frame_count, fps_time):
        pass

    @abstractmethod
    def display_frame(self, detected_frame, fps):
        pass

    @abstractmethod
    def process_frame(self, frame, elapsed_time):
        pass

    @abstractmethod
    def record_screen(self):
        pass

    @abstractmethod
    def start_recording(self):
        pass

    @abstractmethod
    def stop_recording(self):
        pass

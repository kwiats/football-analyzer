import os

TORCH_DEVICE = os.getenv('TORCH_DEVICE')
RECORDER_FPS = int(os.getenv('RECORDER_FPS', 30))
QUEUE_MAX_SIZE = int(os.getenv('QUEUE_MAX_SIZE', 100))
YOLO_MODEL_PATH = os.getenv('MODEL_PATH', 'yolov10n.pt')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'output.mp4')
SAVE_FILE_OUTPUT = os.getenv('SAVE_FILE_OUTPUT', 'y').lower() == 'y'
DISPLAY_SCREEN = os.getenv('DISPLAY_SCREEN', 'n').lower() == 'y'
LIST_WINDOWS = os.getenv('LIST_WINDOWS', 'n').lower() == 'y'
APP_NAME = os.getenv('APP_NAME')
VIDEO_FORMAT = os.getenv('VIDEO_FORMAT', 'mp4v')
DETECTED_SCREEN_NAME = os.getenv('DETECTED_SCREEN_NAME', 'Detected Frame')
YOLO_MODEL_LOGS = os.getenv('YOLO_MODEL_LOGS', 'n').lower() == 'y'
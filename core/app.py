import argparse
import queue
import sys

import torch
from ultralytics import YOLO

from config import QUEUE_MAX_SIZE, YOLO_MODEL_PATH
from core.processor import ScreenProcessor
from detector.object_detector import ObjectDetector
from recorder.screen_recorder import ScreenRecorder
from windows.window_utils import list_windows, get_window_bounds


class FootballMatchAnalyzerApp:
    def __init__(self):
        self.args = None

    def display_menu(self):
        print("Menu:")
        print("1. List available windows")
        print("2. Record a specific application window")
        print("3. Exit")
        choice = input("Enter your choice: ")
        return choice

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Screen recording with object detection.')
        parser.add_argument('--list-windows', action='store_true', help='List available windows and exit.')
        parser.add_argument('--app-name', type=str, help='Name of the application window to record.')
        parser.add_argument('--output-file', type=str, default='output.mp4', help='Output file name.')
        parser.add_argument('--display-screen', action='store_true', help='Display the screen while recording.')
        self.args = parser.parse_args()

    def run(self):
        self.parse_arguments()

        while len(sys.argv) == 1:
            print('No arguments provided')
            choice = self.display_menu()
            if choice == '1':
                windows = list_windows()
                for i, (owner, name) in enumerate(windows):
                    print(f"{i + 1}. {owner} - {name}")
            elif choice == '2':
                self.args.app_name = input("Enter the application name: ").strip()
                self.args.output_file = input("Enter the output file name (default: output.mp4): ") or 'output.mp4'
                self.args.display_screen = input("Display the screen while recording? (y/n): ").lower() == 'y'
                break
            elif choice == '3':
                print("Exiting...")
                return
            else:
                print("Invalid choice. Please try again.")

        if self.args.list_windows:
            windows = list_windows()
            for i, (owner, name) in enumerate(windows):
                print(f"{i + 1}. {owner} - {name}")
            return

        if not self.args.app_name:
            print("Please provide the application name using --app-name.")
            return

        region = get_window_bounds(self.args.app_name)
        if region is None:
            print(f"Could not find window with name {self.args.app_name}")
            return

        if torch.backends.mps.is_available():
            print("Using MPS (Metal Performance Shaders)")
            device = torch.device("mps")
        elif torch.cuda.is_available():
            print("Using CUDA")
            device = torch.device("cuda")
        else:
            print("Using CPU")
            device = torch.device("cpu")

        model = YOLO(YOLO_MODEL_PATH).to(device)
        recorder = ScreenRecorder(self.args.output_file, region)
        processed_frame_queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)
        detector = ObjectDetector(model, recorder.frame_queue, processed_frame_queue)

        processor = ScreenProcessor(recorder, detector)
        print("Commands: 'r' to start recording, 's' to stop recording, 'q' to exit.")
        while True:
            command = input("Enter command: ").strip().lower()
            if command == 'r':
                processor.display()
            elif command == 's':
                processor.stop_processing()
            elif command == 'q':
                print("Exiting...")
                break

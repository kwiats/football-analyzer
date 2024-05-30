import argparse
import queue
import sys

import torch
from ultralytics import YOLO

from config import QUEUE_MAX_SIZE, YOLO_MODEL_PATH
from detector.object_detector import ObjectDetector, display_processed_frames
from recorder.screen_recorder import ScreenRecorder
from windows.window_utils import list_windows, get_window_bounds

player_positions = []


def display_menu():
    print("Menu:")
    print("1. List available windows")
    print("2. Record a specific application window")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice


def main():
    parser = argparse.ArgumentParser(description='Screen recording with object detection.')
    parser.add_argument('--list-windows', action='store_true', help='List available windows and exit.')
    parser.add_argument('--app-name', type=str, help='Name of the application window to record.')
    parser.add_argument('--output-file', type=str, default='output.mp4', help='Output file name.')
    parser.add_argument('--display-screen', action='store_true', help='Display the screen while recording.')
    args = parser.parse_args()

    while len(sys.argv) == 1:
        print('No arguments provided')
        choice = display_menu()
        if choice == '1':
            windows = list_windows()
            for i, (owner, name) in enumerate(windows):
                print(f"{i + 1}. {owner} - {name}")
        elif choice == '2':
            args.app_name = input("Enter the application name: ").strip()
            args.output_file = input("Enter the output file name (default: output.mp4): ") or 'output.mp4'
            args.display_screen = input("Display the screen while recording? (y/n): ").lower() == 'y'
            break
        elif choice == '3':
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please try again.")

    if args.list_windows:
        windows = list_windows()
        for i, (owner, name) in enumerate(windows):
            print(f"{i + 1}. {owner} - {name}")
        return

    if not args.app_name:
        print("Please provide the application name using --app-name.")
        return

    region = get_window_bounds(args.app_name)
    if region is None:
        print(f"Could not find window with name {args.app_name}")
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
    recorder = ScreenRecorder(args.output_file, region)
    processed_frame_queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)

    detector = ObjectDetector(model, recorder.frame_queue, processed_frame_queue)

    print("Commands: 'r' to start recording, 's' to stop recording, 'q' to exit.")
    while True:
        command = input("Enter command: ").strip().lower()
        if command == 'r':
            recorder.start_recording()
            detector.start_processing()
            display_processed_frames(detector.processed_frame_queue)
        elif command == 's':
            recorder.stop_recording()
            detector.stop_processing()
        elif command == 'q':
            recorder.stop_recording()
            detector.stop_processing()
            print("Exiting...")
            break


if __name__ == "__main__":
    # fig, ax = create_pitch()
    # ani = FuncAnimation(fig, update_plot, fargs=(ax, player_positions), interval=66,
    #                     cache_frame_data=False)
    # plt.show()

    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")

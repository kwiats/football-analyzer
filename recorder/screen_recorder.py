import time

import cv2
import mss
import numpy as np

from detector.detect_objects import detect_objects

recording = False


def set_recording(value):
    global recording
    recording = value


def record_screen(output_file, display_screen, model, region):
    global recording
    global player_positions
    with mss.mss() as sct:
        monitor = {"top": int(region[1]), "left": int(region[0]), "width": int(region[2]), "height": int(region[3])}
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, 30.0, (monitor["width"], monitor["height"]))

        start_time = time.time()
        frame_count = 0
        fps = 0
        fps_time = time.time()
        one_sec_frame = 0

        while recording:
            frame_start_time = time.time()
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            detected_frame, player_positions = detect_objects(frame, model)
            # detected_frame = frame
            out.write(frame)

            frame_count += 1
            if time.time() - fps_time >= 1:
                fps = frame_count
                frame_count = 0
                fps_time = time.time()
            print(f"FPS: {fps}")

            cv2.rectangle(detected_frame, (5, 5), (150, 40), (0, 0, 0), -1)
            cv2.putText(detected_frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if display_screen:
                cv2.imshow("Screen", detected_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            elapsed_time = time.time() - start_time
            if int(elapsed_time) > one_sec_frame:
                process_frame(frame, elapsed_time)  # Wyciągnij i zapisz jedną klatkę na sekundę
                one_sec_frame += 1

        out.release()
        cv2.destroyAllWindows()


def process_frame(frame, elapsed_time):
    filename = f"output/frame_at_{int(elapsed_time)}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")


def start_recording(output_file, display_screen, model, region):
    global recording
    recording = True
    print('start_recording')
    record_screen(output_file, display_screen, model, region)


def stop_recording():
    global recording
    recording = False

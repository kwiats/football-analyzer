import cv2


def save_frame_per_second(frame, second):
    filename = f"frame_{second}.jpg"
    cv2.imwrite(filename, frame)
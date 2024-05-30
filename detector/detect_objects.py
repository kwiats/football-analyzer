import cv2


def detect_objects(frame, model):
    player_positions = []
    results = model(frame)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy.tolist()[0]
            conf = box.conf.item()
            cls = box.cls.item()
            label = f"{model.names[int(box.cls.item())]} {box.conf.item():.2f}"

            if cls == 0:  # Assuming class '0' is for players
                # Calculate the center of the bounding box
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                player_positions.append((center_x, center_y))

            frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            frame = cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0),
                                2)

    return frame, player_positions

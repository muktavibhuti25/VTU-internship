import cv2
from ultralytics import YOLO
import os

def process_video(input_path, output_folder):
    print("Starting processing...")

    model = YOLO("yolov8s.pt")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("ERROR: Cannot open video")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25

    output_path = os.path.join(output_folder, "output.avi")

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'XVID'),
        fps,
        (width, height)
    )

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
                    cv2.putText(frame, label, (x1,y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

    print("✅ Output saved at:", output_path)
    return "output.avi"
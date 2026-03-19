import cv2
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
frame_count = 0
last_annotated_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1) #отражение
    frame_count += 1
    if frame_count % 3 == 0:
        results = model.predict(
            frame, 
            verbose=False,
            conf=0.3,
            iou=0.5,
            max_det=10,
            imgsz=320
        )
        
        last_annotated_frame = results[0].plot()
    
    if last_annotated_frame is not None:
        display_frame = last_annotated_frame
    else:
        display_frame = frame
    cv2.imshow("Detection", display_frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

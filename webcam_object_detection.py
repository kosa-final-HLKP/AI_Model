import cv2

from yolov8 import YOLOv8

# Initialize the webcam
cap = cv2.VideoCapture(1)

# Initialize YOLOv8 object detector
model_path = "/Users/jihyun/PycharmProjects/AI_Model/models/best.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.5, iou_thres=0.5)

cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
while cap.isOpened():

    # Read frame from the video
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    if not ret:
        break

    # Update object localizer
    boxes, scores, class_ids = yolov8_detector(frame)

    combined_img = yolov8_detector.draw_detections(frame)
    cv2.imshow("Detected Objects", combined_img)

    # Press key q to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

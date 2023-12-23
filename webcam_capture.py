import os
from datetime import datetime

import cv2
import numpy as np
from yolov8 import YOLOv8

import requests

# == Model =============================================================================================================
# Initialize YOLOv8 object detector
model_path = "/Users/jihyun/PycharmProjects/AI_Model/models/best.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.5, iou_thres=0.5)
# ======================================================================================================================

# == alarm parameter ===================================================================================================
# Parameters for notification
positive_limit = 10
class_id_positive = 3
confidence_threshold = 0.7

# Variables for tracking consecutive frames
positive_frames = 0
continous_frames = 0
# ======================================================================================================================

# == api ===============================================================================================================
def send_get_request(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text  # You can return the response content or other relevant information
    except requests.exceptions.RequestException as e:
        print(f"Failed to send GET request: {e}")
        return None

# API endpoint URL
positive_api_url = "https://wondrous-pudding-b2d415.netlify.app/api/push/smile"
# ======================================================================================================================

# == webcam ============================================================================================================
# Initialize the webcam
cap = cv2.VideoCapture(1)

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

    # == 웃음 감지 후 알림 및 캡쳐 ===========================================================================================
    # Check if class_id_positive has confidence above the threshold
    if class_id_positive in class_ids and np.max(scores[class_ids == class_id_positive]) > confidence_threshold:
        positive_frames += 1
        if positive_frames == positive_limit:
            print(f"Class {class_id_positive} : {positive_frames} consecutive frames!")
            print("positive detection")
            cv2.putText(combined_img, "POSITIVE DETECTION", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Send GET request and print the response
            response_content = send_get_request(positive_api_url)
            if response_content is not None:
                print(f"Response from the server:\n{response_content}")

        if positive_limit < positive_frames < positive_limit + 6:
            # 여기에서 프레임을 이미지 파일로 저장하거나 추가 작업을 수행할 수 있습니다.
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_dir = "/Users/jihyun/PycharmProjects/BebeFace/save/capture"
            file_name = f"capture_{timestamp}.png"
            file_path = os.path.join(save_dir, file_name)
            cv2.imwrite(file_path, frame)
            print(f"Saved {file_name}")
    else:
        positive_frames = 0


    # Press key q to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
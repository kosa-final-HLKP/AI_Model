import os
import datetime

import cv2
import numpy as np
from yolov8 import YOLOv8

import requests


# == Model =============================================================================================================
# Initialize YOLOv8 object detector
model_path = "/Users/jihyun/PycharmProjects/BebeFace/models/best.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.5, iou_thres=0.5)
# ======================================================================================================================

# == alarm & capture parameter =========================================================================================
# Parameters for notification
back_limit = 10
negative_limit = 10
positive_limit = 10

back_interval = 10
negative_interval = 20

class_id_back = 0
class_id_negative = 1
class_id_positive = 3
confidence_threshold = 0.7

# Variables for tracking consecutive frames
back_frames = 0
negative_frames = 0
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
back_api_url = "https://wondrous-pudding-b2d415.netlify.app/api/push/back"
negative_api_url = "https://wondrous-pudding-b2d415.netlify.app/api/push/cry"
positive_api_url = "https://wondrous-pudding-b2d415.netlify.app/api/push/smile"
# ======================================================================================================================


# == webcam ============================================================================================================
# Initialize the webcam
cap = cv2.VideoCapture(1)
cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set the width of the frames
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1240)  # Set the height of the frames


while cap.isOpened():

    # Read frame from the video
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    if not ret:
        break


    # Update object localizer
    boxes, scores, class_ids = yolov8_detector(frame)

    combined_img = yolov8_detector.draw_detections(frame)


    # == 뒷통수 감지 후 알림 ================================================================================================
    # Check if class_id_back has confidence above the threshold
    if (back_frames == 0) and (class_id_back in class_ids) and (np.max(scores[class_ids == class_id_back]) > confidence_threshold):
        back_frames += 1

    elif (back_frames > 0) and (class_id_back in class_ids) and (np.max(scores[class_ids == class_id_back]) > 0.4):
        back_frames += 1
        if back_frames == back_limit:
            print(f"Class {class_id_back} : {back_frames} consecutive frames")
            cv2.putText(combined_img, "BACK DETECTION", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print("back detection")

            # Send GET request and print the response
            response_content = send_get_request(back_api_url)
            if response_content is not None:
                print(f"Response from the server:\n{response_content}")

        elif back_frames > back_limit:
            continous_frames += 1

            if continous_frames % back_interval == 0:
                print(f"Class {class_id_back} : {continous_frames} continous frames")
                cv2.putText(combined_img, "BACK DETECTION", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print("back detection")

                # Send GET request and print the response
                response_content = send_get_request(back_api_url)
                if response_content is not None:
                    print(f"Response from the server:\n{response_content}")

    else:
        back_frames = 0


    # == 울음 감지 후 알림 =================================================================================================
    # Check if class_id_negative has confidence above the threshold
    if (negative_frames == 0) and (class_id_negative in class_ids) and (np.max(scores[class_ids == class_id_negative]) > confidence_threshold):
        negative_frames += 1

    elif (negative_frames > 0) and (class_id_negative in class_ids) and (np.max(scores[class_ids == class_id_negative]) > 0.4):
        negative_frames += 1
        if negative_frames == negative_limit:
            print(f"Class {class_id_negative} : {negative_frames} consecutive frames")
            cv2.putText(combined_img, "NEGATIVE DETECTION", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print("negative detection")

            # Send GET request and print the response
            response_content = send_get_request(negative_api_url)
            if response_content is not None:
                print(f"Response from the server:\n{response_content}")

        elif negative_frames > negative_limit:
            continous_frames += 1

            if continous_frames % negative_interval == 0:
                print(f"Class {class_id_back} : {continous_frames} continous frames")
                cv2.putText(combined_img, "BACK DETECTION", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print("back detection")

                # Send GET request and print the response
                response_content = send_get_request(back_api_url)
                if response_content is not None:
                    print(f"Response from the server:\n{response_content}")

    else:
        negative_frames = 0


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


    cv2.imshow("Detected Objects", combined_img)

    # Press key q to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
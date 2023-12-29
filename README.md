# Requirements

 * Check the **requirements.txt** file.
 * For ONNX, if you have a NVIDIA GPU, then install the **onnxruntime-gpu**, otherwise use the **onnxruntime** library.
 * To use this model, you must have a model in the form of onnx. This GitHub does not include a model, so please contact us by email if you want to run it

# Installation
```shell
git clone https://github.com/jihyun-log/AI_Model-BebeFace_KOSA-project.git
cd AI_Model-BebeFace_KOSA-project
pip install -r requirements.txt
```
### ONNX Runtime
For Nvidia GPU computers:
`pip install onnxruntime-gpu`

Otherwise:
`pip install onnxruntime`


# Importance

* There's a part that has to be rerouted unconditionally
* You need to change the best.onnx file in the models folder to your path,
* but there is no best.onnx file on the collar, so please contact me if you need it
* change the underlying code to model_path = "your path" for each file
```shell 
== Model =============================================================================================================
Initialize YOLOv8 object detector
model_path = "/Users/{your path}/best.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.5, iou_thres=0.5)
======================================================================================================================
```

# 24 Hours Monitoring System -  Baby Status Detection

 * **24 Hours Monitoring System : Main**:
 ```shell
 python main.py
 ```

 * **Webcam Baby Status Detection**:
 ```shell
 python webcam_object_detection.py
 ```

 * **24 Hours Monitoring System : Alarm - Back, Negative Status Detection**:
 ```shell
 python webcam_alarm.py
 ```

 * **24 Hours Monitoring System : Capture and Alarm - Positive Status Detection**:
 ```shell
 python webcm_capture.py
 ```
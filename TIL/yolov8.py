from ultralytics import YOLO
# 가장 가벼운 인체/사물 인지용 nano 모델을 ONNX 포맷으로 내보내기
YOLO("yolov8n.pt").export(format="onnx")
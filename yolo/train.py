from ultralytics import YOLO

model = YOLO("yolov8n.yaml")

results = model.train(data="/Users/dharaneswarang/Desktop/tensorflow/yolo/data.yaml",epochs = 5)

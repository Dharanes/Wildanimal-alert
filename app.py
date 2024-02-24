import io
from PIL import Image
import os
import cv2
import numpy as np 
from ultralytics import YOLO
from current_location import Location
from send_email import EmailSender

from flask import Flask, render_template, request, send_from_directory, Response, redirect, url_for

app = Flask(__name__)
location = Location()
mail = EmailSender('20euit029@skcet.ac.in','bnqmlvbznuihvafi')


animalsClass = ['tiger','elephant','rhino','lion','zebra']

@app.route("/")
def entry_point():
    return render_template('dummy.html')

@app.route("/", methods=["GET", "POST"])
def predict_img():
    predicted_classes = []
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath, 'upload', f.filename)
            print('Upload folder is ', filepath)
            f.save(filepath)

            file_extension = f.filename.rsplit('.', 1)[1].lower()

            if file_extension in ['jpg', 'jpeg', 'png']:
                img = cv2.imread(filepath)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                image = Image.open(io.BytesIO(frame))

                yolo = YOLO('yolov8x.pt')
                detections = yolo.predict(filepath, save=True)
                for detection in detections:
                    boxes = detection.boxes.xyxy.cpu().tolist()
                    classes = detection.names
                    clss = detection.boxes.cls.cpu().tolist()
                    for index in clss:
                        index = int(index)
                        predicted_classes.append(classes[index])
                    print(predicted_classes)
                
                get_location = location.geo_data['city']+','+location.geo_data['region']
                predicts = set(predicted_classes)
                animals = ""
                print(animalsClass)
                for i in predicts:
                    if i in animalsClass:
                        animals = animals+" "+i
                if animals!="":
                    mail.send_email('Animal Detected',animals+' these animals are detected in this area '+get_location)

                # return render_template('dummy.html', classes=predicted_classes)

                return display_image(f.filename)

            elif file_extension == 'mp4':
                video_path = filepath
                cap = cv2.VideoCapture(video_path)
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))
                model = YOLO('yolov8n.pt')

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    results = model(frame, save=True)
                    
                    for result in results:
                        frame_ = result.plot()
                        out.write(frame_)
                cap.release()
                out.release()
                return video_feed()
    return render_template('dummy.html')

@app.route('/<filename>')
def display_image(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = os.path.join(folder_path, latest_subfolder)
    files = os.listdir(directory)
    latest_file = files[0]
    filename = os.path.join(folder_path, latest_subfolder, latest_file)
    return send_from_directory(directory, latest_file)

def get_frame():
    folder_path = os.getcwd()
    mp4_file = 'output.mp4'
    video = cv2.VideoCapture(mp4_file)
    while True:
        success, image = video.read()
        if not success:
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    # return render_template('video.html')

@app.route("/video_feed")
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

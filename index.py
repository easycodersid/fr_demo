import base64
import glob
import json
import os

import face_recognition
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
eventlet.monkey_patch()

@socketio.on('message')
def handle_message(message):
    image_data = message['content']
    image_data = image_data.split(",")
    name = message['name']
    # milli = message['milliseconds']
    folder = "temp"
    path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(path):
        os.mkdir(path)
        with open(os.path.join(path, name + ".jpg"), "wb") as fh:
            fh.write(base64.b64decode(image_data[1]))
    else:
        with open(os.path.join(path, name + ".jpg"), "wb") as fh:
            fh.write(base64.b64decode(image_data[1]))

    # Load the jpg files into numpy arrays
    # biden_image = face_recognition.load_image_file("jk.jpg")
    # obama_image = face_recognition.load_image_file("obama.jpg")
    # unknown_image = face_recognition.load_image_file("D:\WORLDS SIMPLEST FACIAL RECOGNITION\\face_recognition\examples\\temp\demo.jpg")
    # #print(unknown_image)
    # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[1]
    # print(type(unknown_face_encoding))
    known_faces = []
    unknown_face_encoding = ""
    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.

    if os.path.exists(os.path.join(os.getcwd() + "\\" + name)):
        try:

            for filename in glob.glob(os.path.join(os.getcwd()+"\\"+name, '*.jpg')):
                with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                    known_faces.append(face_recognition.face_encodings(face_recognition.load_image_file(f))[0])
            for filename in glob.glob(os.path.join(os.getcwd()+"\\temp", '*.jpg')):
                with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                    unknown_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(f))[0]

        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()

        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

        try:
            print("Is the unknown face a picture of demo? {}".format(results[0]))
            print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
            status = []
            if results[0]:
                stat = {"status": "Verified"}
                status.append(stat)
            else:
                stat = {"status": "Not Verified"}
                status.append(stat)
            emit('message', json.dumps(stat))
        except: emit('message', json.dumps({"message": "Some error"}))
    else: emit('message', json.dumps({"message": "Unknown user! Training data does not exist."}))
    # os.remove(os.getcwd()+"\\temp")
    shutil.rmtree(os.getcwd()+"\\temp",ignore_errors= False)
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
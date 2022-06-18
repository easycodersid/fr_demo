import base64
import face_recognition
import glob
import os
from flask import Flask
from flask_cors import CORS
import json

from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
app.debug = True
# CORS(app)

@app.route("/", methods=["GET", "POST"])
def api():
    if request.mimetype == 'application/json':
        req_data = request.get_json()
    else:
        req_data = request.form
    image_data = req_data['content']
    image_data = image_data.split(",")
    name = req_data['name']
    # milli = req_data['milliseconds']
    folder = "temp"
    path = os.path.join("/", folder)
    if not os.path.exists(path):
        os.mkdir(path)
        with open(os.path.join(path, name+".jpg"), "wb") as fh:
            fh.write(base64.b64decode(image_data[1]))
    else:
        with open(os.path.join(path, name+".jpg"), "wb") as fh:
            fh.write(base64.b64decode(image_data[1]))


    # Load the jpg files into numpy arrays
    # biden_image = face_recognition.load_image_file("jk.jpg")
    # obama_image = face_recognition.load_image_file("obama.jpg")
    # unknown_image = face_recognition.load_image_file("D:\WORLDS SIMPLEST FACIAL RECOGNITION\\face_recognition\examples\\temp\demo.jpg")
    # #print(unknown_image)
    # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[1]
    # print(type(unknown_face_encoding))
    known_faces = []

    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    try:
        for filename in glob.glob(os.path.join("/demo", '*.jpg')):
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                known_faces.append(face_recognition.face_encodings(face_recognition.load_image_file(f))[0])
        for filename in glob.glob(os.path.join("/temp", '*.jpg')):
            with open(os.path.join(os.getcwd(), filename), 'rb') as f:
                unknown_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(f))[0]

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()
    #

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

    print("Is the unknown face a picture of demo? {}".format(results[0]))
    print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
    status=[]
    if results[0]:
        stat={"status":"Verified"}
        status.append(stat)
    else:
        stat = {"status": "Not Verified"}
        status.append(stat)
    return json.dumps(stat)

if __name__ == '__main__':

    app.run(host='0.0.0.0')
    app.debug = True

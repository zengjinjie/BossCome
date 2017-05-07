import cv2
import urllib.request
import numpy as np
import face_recognition
import random
import time

stream = urllib.request.
bytes = bytes()
boss_image = face_recognition.load_image_file("IMG_1778.JPG")
boss_face_encoding = face_recognition.face_encodings(boss_image)[0]
face_locaions = []
face_encodings = []
face_names = []
k = 0
h = 0

while True:
    bytes += stream.read(512)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    k += 1
    if a != -1 and b != -1:
        h += 1
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        face_locaions = face_recognition.face_locations(i)
        face_encodings = face_recognition.face_encodings(i, face_locaions)

        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([boss_face_encoding], face_encoding)
            name = "Unknown"

            if match[0]:
                name = "Boss"
                print("Boss is coming")

        cv2.imshow('Video', i)
        if cv2.waitKey(1) == 27:
            exit(0)
    print(k, h)
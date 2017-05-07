import cv2
import numpy as np
from urllib import request
import face_recognition
import random
import time

xiaomi_url = "http://192.168.2.112:8080/shot.jpg"
meizu_url = "http://192.168.1.152:8080/shot.jpg"
test_url = "http://172.26.54.57:8080/shot.jpg"
boss_image = face_recognition.load_image_file("IMG_1778.JPG")
boss_face_encoding = face_recognition.face_encodings(boss_image)[0]
face_locaions = []
face_encodings = []
face_names = []
k = 0

while True:
    with request.urlopen(meizu_url) as f:
        data = f.read()
        # print(f.status, f.reason)
        # for k, v in f.getheaders():
        #     print('%s: %s' % (k, v))
        # print(data)
        nparr = np.fromstring(data, np.uint8)
        # print(nparr)
        # print()
        i = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        face_locaions = face_recognition.face_locations(i)
        face_encodings = face_recognition.face_encodings(i, face_locaions)

        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([boss_face_encoding], face_encoding, tolerance=0.4)
            name = "Unknown"

            if match[0]:
                name = "Boss"
                print("Boss is coming")

        cv2.imshow('JPEG', i)
        k += 1
        print(k)
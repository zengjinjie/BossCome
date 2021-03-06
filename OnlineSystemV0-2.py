#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
import os, time, random
import urllib.request
import numpy as np
import face_recognition
import cv2
import asyncio
import random
import websockets
import threading
import time

connected = set()

def notice(q):
    async def notify(websocket, path):
        global connected
        connected.add(websocket)
        while True:
            value = q.get(True)
            print("Get %s from queue." %value)
            print(len(connected))
            await asyncio.wait([ws.send("Boss is coming for %s times" %value) for ws in connected])
            await asyncio.sleep(0.1)

    start_server = websockets.serve(notify, '10.8.0.10', 5678)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()



def detect(q):
    realsystem_url = "http://219.242.112.243:8080/shot.jpg"
    boss_image = face_recognition.load_image_file("zengjinjie.jpg")
    other_image = face_recognition.load_image_file("zhaoyun.jpg")
    boss_face_encoding = face_recognition.face_encodings(boss_image)[0]
    other_face_encoding = face_recognition.face_encodings(other_image)[0]
    known_face_encodings = [boss_face_encoding, other_face_encoding]

    face_locaions = []
    face_encodings = []
    face_names = []
    k = 0

    while True:
        with urllib.request.urlopen(realsystem_url) as f:
            data = f.read()
            nparr = np.fromstring(data, np.uint8)
            i = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            face_locaions = face_recognition.face_locations(i)
            face_encodings = face_recognition.face_encodings(i, face_locaions)

            face_names = []
            for face_encoding in face_encodings:
                match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
                name = "Unknown"
                if match[0]:
                    name = "Boss"
                    print("Boss is coming", time.ctime())
                    k += 1
                    q.put(k)

if __name__ == '__main__':
    q = Queue()
    pd = Process(target=detect, args=(q,))
    pn = Process(target=notice, args=(q,))
    pn.start()
    pd.start()
    pd.join()
    pn.terminate()

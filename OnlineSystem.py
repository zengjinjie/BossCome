import urllib.request
import numpy as np
import face_recognition
import cv2
import asyncio
import random
import websockets
import threading
import time

async def notify(websocket, path):
    while True:
        global s
        # print(s)
        if(s):
            await websocket.send("Boss is coming")
            s = False
        await asyncio.sleep(1)

class DetectThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        realsystem_url = "http://219.242.112.243:8080/shot.jpg"
        boss_image = face_recognition.load_image_file("IMG_1778.JPG")
        boss_face_encoding = face_recognition.face_encodings(boss_image)[0]
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
                    match = face_recognition.compare_faces([boss_face_encoding], face_encoding, tolerance=0.4)
                    name = "Unknown"
                    if match[0]:
                        name = "Boss"
                        print("Boss is coming")
                        global s
                        s = True
                k += 1
                # print(k)

def main():
    global s
    s = False
    detectThread = DetectThread()
    detectThread.start()
    print("Detect thread started")

    start_server = websockets.serve(notify, '10.8.0.10', 5678)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()
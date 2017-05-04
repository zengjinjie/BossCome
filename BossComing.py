import face_recognition
import cv2

import asyncio
import datetime
import random
import websockets
import threading
import time

async def time1(websocket, path):
    while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
        global s
        print(s)
        if(s) :
            await websocket.send('Boss is coming')
            s = False
        # await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

def notice(s):
    while True:
        time.sleep(1);
        print(s)

# class Notice(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         start_server = websockets.serve(time1, '127.0.0.1', 5678)
#         asyncio.get_event_loop().run_until_complete(start_server)
#         asyncio.get_event_loop().run_forever()



class DetectTread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("IMG_1778.JPG")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            # Loop through each face in this frame of video
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces([obama_face_encoding], face_encoding, tolerance=0.5)

                name = "Idiot"
                if match[0]:
                    name = "Boss"
                    print('Zengjinjie is coming')
                    global s
                    s = True
                    # global s
                    # mutex.acquire()
                    # s = True
                    # mutex.release()

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


global s
s = False

# thread1 = Notice()
thread2 = DetectTread()
# thread1.start()
thread2.start()

print('abcdefg')
start_server = websockets.serve(time1, '127.0.0.1', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

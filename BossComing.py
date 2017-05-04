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
        video_capture = cv2.VideoCapture(0)

        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("IMG_1778.JPG")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        i = 0
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
                    name = "Unknown"

                    if match[0]:
                        name = "Boss"
                        i = i + 1
                        print('Zengjinjie is coming')
                        print(i)
                        global s
                        s = True

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

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

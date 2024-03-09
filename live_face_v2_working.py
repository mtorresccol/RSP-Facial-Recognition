import face_recognition
import cv2
import numpy as np
from playsound import playsound
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials 
import time
from datetime import date




# Setup for current time and date
today = date.today()
t = time.localtime()
current_time = time.strftime("%H : %M : %S", t)

# Google Sheets API Authentication setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/admin/Downloads/security-lock-cloud-data-6b71e326c161.json', scope)
client = gspread.authorize(creds)
sheet = client.open('entrance_log').sheet1
#sheet.share('mtorrescohencol@gmail.com', perm_type='user', role='writer')



# vars for authorization logic
check = 0
auth_check = 0

# Capture webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Authorized face(Mateo).
authorized_image = face_recognition.load_image_file("mateo.jpg")
authorized_face_encoding = face_recognition.face_encodings(authorized_image)[0]

# Authorized face(Nick).
nick_image = face_recognition.load_image_file("Nick.jpg")
nick_face_encoding = face_recognition.face_encodings(nick_image)[0]


# arrays of known face encodings and their names
known_face_encodings = [
    authorized_face_encoding,
    nick_face_encoding
]
known_face_names = [
    "Mateo",
    "Nick"
]


state = True
# Logic for authorization in security application and display
while state == True:

    
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
        
        
        if auth_check >= 6:
            state = False
            playsound('/Users/admin/RSP/Authorized.mp3')
            sheet.append_row(data)
        elif check == 20:
             state = False
             playsound('/Users/admin/RSP/Unauthorized.mp3')
             sheet.append_row(data)
        
        
        
        # known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            
            name = known_face_names[best_match_index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 2, (255, 0, 0), 1)
            auth_check +=1
            data = [str(name), str(today), str(current_time)]
            print("Authorized " + str(auth_check) + " times" )



        else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 2, (255, 255, 255), 1)
                check += 1
                data = [str(name), str(today), str(current_time)]
                print("Unauthorized " + str(check) + " times" )
        

        
        
        

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()



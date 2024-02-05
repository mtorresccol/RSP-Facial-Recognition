import face_recognition
import cv2
import numpy as np
from playsound import playsound

# vars for authorization logic
check = 0
auth_check = 0

# Capture webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Authorized face.
authorized_image = face_recognition.load_image_file("mateo.jpg")
authorized_face_encoding = face_recognition.face_encodings(authorized_image)[0]

# Authorized face.
biden_image = face_recognition.load_image_file("ben.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]


# arrays of known face encodings and their names
known_face_encodings = [
    authorized_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Mateo",
    "Joe Biden"
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
        elif check == 20:
             state = False
             playsound('/Users/admin/RSP/Unauthorized.mp3')

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            
            name = known_face_names[best_match_index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 2, (255, 0, 0), 1)
            auth_check +=1
            print("Authorized " + str(auth_check) + " times" )



        else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 2, (255, 255, 255), 1)
                check += 1
                print("Unauthorized " + str(check) + " times" )
        

        
        
        

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()



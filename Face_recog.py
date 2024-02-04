import face_recognition
import numpy as np
import cv2
import face_recognition_models

mateo = face_recognition.load_image_file("mateo.jpg")
mateo_enc = face_recognition.face_encodings(mateo)[0]

not_mateo = face_recognition.load_image_file("mateo.jpg")
not_mateo_enc = face_recognition.face_encodings(not_mateo)[0]
print(not_mateo)
        
comparison = face_recognition.compare_faces([mateo_enc], not_mateo_enc)

if comparison == True:
    print("This is Mateo!")
else:
    print("this is not Mateo!")

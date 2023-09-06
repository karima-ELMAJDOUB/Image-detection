# -*- coding: utf-8 -*-
"""projet.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kn2B8eLCXe6PrQNluNmUJ76wZoxpEmTO
"""

!wget   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

!bunzip2 /content/shape_predictor_68_face_landmarks.dat.bz2
datFile =  "/content/shape_predictor_68_face_landmarks.dat"

import cv2
import dlib
import numpy as np
from imutils import face_utils
from google.colab.patches import cv2_imshow

def distance(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def eye_AR(a,b,c,d,e,f):
	up = distance(b,d) + distance(c,e)
	down = distance(a,f)
	ratio = up/(2.0*down)


	if(ratio>0.25):
		return 2
	elif(ratio>0.21 and ratio<=0.25):
		return 1
	else:
		return 0

frame=cv2.imread('image.jpg')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(datFile)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = detector(frame)

for face in faces:
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    landmarks = predictor(gray, face)
    landmarks = face_utils.shape_to_np(landmarks)
    left_eye = eye_AR(landmarks[36],landmarks[37],landmarks[38], landmarks[41], landmarks[40], landmarks[39])
    right_eye = eye_AR(landmarks[42],landmarks[43],landmarks[44], landmarks[47], landmarks[46], landmarks[45])

if(left_eye==0 or right_eye==0):
        status="il dort "
        color = (255,0,0)

  elif(left_eye==1 or right_eye==1):
        status="il va dormir"
        color = (0,0,255)

  else:
        status="Reveille"
        color = (0,255,0)

cv2.putText(frame, status, (x1, y1-2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

for n in range(0, 68):
      (x,y) = landmarks[n]
      cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

cv2_imshow(frame)
import numpy as np
import mediapipe as mp
import handTrackingModule as htm
from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import socket
import math

#parameter
width, height = 1280, 720
#Webcam
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#Hand Detector
detector = HandDetector(maxHands=2, detectionCon=0.8)

#Find Function
x = [300, 245, 200, 170., 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2) # y = Ax^2 + Bx + C

#Commmunication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True :
    ret, img = cap.read()

    #Hands
    hands, img = detector.findHands(img)
    data1 = []
    data2 = []
    data = []

    if len(hands)==2:
        hand1 = hands[0]
        lmList1 = hand1['lmList']

        hand2 = hands[1]
        lmList2 = hand2['lmList']

        if ((lmList1[0] != None) and (lmList2[0] != None)):
            handType1 = hand1['type']
            handType2 = hand2['type']

            #measuring distance
            x1, y1, z1 = lmList1[5]
            x2, y2, z2 = lmList1[17]
            x3, y3, z3 = lmList2[5]
            x4, y4, z4 = lmList2[17]
            distance1 = int(math.sqrt((y2 -y1)**2 + (x2 - x1) ** 2))
            distance2 = int(math.sqrt((y4 - y3) ** 2 + (x4 - x3) ** 2))
            A, B, C = coff
            distanceCM1 = A*distance1**2 + B*distance1 + C - 10 #in cm
            distanceCM2 = A * distance2 ** 2 + B * distance2 + C - 10  # in cm

            if str("Left") == handType1:
                data.extend([distanceCM1, distanceCM2])
                for lm1 in lmList1:
                    # data1.extend([1, distanceCM, lm[0], height - lm[1], lm[2]])
                    # data.extend([distanceCM1, lm[0], height - lm[1], lm[2], distanceCM2, lmList2[0], height - lmList2[1], lmList2[2]])
                    data.extend([lm1[0], height - lm1[1], lm1[2]])
                    # print(data1)
                for lm2 in lmList2:
                    data.extend([lm2[0], height - lm2[1], lm2[2]])

                sock.sendto(str.encode(str(data)), serverAddressPort)
                print(data)

            elif str("Right") == handType1:
                data.extend([distanceCM2, distanceCM1])
                for lm2 in lmList2:
                    # data1.extend([1, distanceCM, lm[0], height - lm[1], lm[2]])
                    # data.extend([distanceCM1, lm[0], height - lm[1], lm[2], distanceCM2, lmList2[0], height - lmList2[1], lmList2[2]])
                    data.extend([lm2[0], height - lm2[1], lm2[2]])
                    # print(data1)
                for lm1 in lmList1:
                    data.extend([lm1[0], height - lm1[1], lm1[2]])

                sock.sendto(str.encode(str(data)), serverAddressPort)
                print(data)

    # sendData = data1.extend(data2)
    # sock.sendto(str.encode(str(sendData)), serverAddressPort)
    # print(sendData)

    cv.imshow("Image", img)
    if cv.waitKey(1) ==  ord('q'):
        break

cap.release()
cv.destroyAllWindows()
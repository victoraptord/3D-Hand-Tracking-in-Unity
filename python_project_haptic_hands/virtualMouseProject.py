import cv2 as cv
import numpy as np
import math
import time
import handTrackingModule as htm
import autopy

wCam, hCam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handTracker(maxHands=1)
wScr, hScr = autopy.screen.size()
frameR = 100 #frame reduction
smoothening = 60

plocX, plocY = 0, 0
clocX, clocY = 0, 0


while True:
    #landmarks
    ret, frame = cap.read()
    frame = detector.handsFinder(frame)
    lmList = detector.positionFinder(frame)

    #fingers
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]


        #fingers check
        fingers = detector.fingersUp()
        cv.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        #index finger
        if fingers[1] == 1 and fingers[2] == 0:
            #coordinate converts

            x3 = np.interp(x1, (frameR,wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR), (0,hScr))

            #smoothening
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #move mouse
            autopy.mouse.move(wScr-x3, y3)
            cv.circle(frame, (x1,y1), 15, (255, 0, 255), cv.FILLED)
            plocX, plocY = clocX, clocY

        #click mode
        if fingers[1] == 1and fingers[2] == 1:
            length, frame, lineInfo = detector.findDistance(8, 12, frame)
            print(length)

            if length < 40:
                cv.circle(frame, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv.FILLED)
                autopy.mouse.click()



    #framerate
    cTime = time.time()
    fps = 1/ (cTime-pTime)
    pTime = cTime
    cv.putText(frame, str(int(fps)), (20,50), cv.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)

    #display
    cv.imshow("Image", frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


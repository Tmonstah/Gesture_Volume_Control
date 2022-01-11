import cv2
import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as hand
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

camW, camH = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)
pTime = 0

detector = hand.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volumeRange = volume.GetVolumeRange()


minVol = volumeRange[0]
maxVol = volumeRange[1]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255,0,255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        length = math.hypot((x2-x1), (y2-y1))
        realVol = np.interp(length, [50, 300], [minVol, maxVol])
        volume.SetMasterVolumeLevel(realVol, None)

        if length <=50:
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img",img)
    cv2.waitKey(1)



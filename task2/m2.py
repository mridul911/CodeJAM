  
from cv2 import cv2
import numpy as np
import math

def dist(x1,y1,x2,y2):
    return np.linalg.norm(np.array([x2-x1,y2-y1]))

def mind(x1o,y1o,x1n,y1n,x2n,y2n):
    per = 70/100
    if dist(x1o,y1o,x1n,y1n) > dist(x1o,y1o,x2n,y2n):
        if x1o*(1+per) > x2n and x1o*(1-per) < x2n and y1o*(1+per) > y2n and y1o*(1-per) < y2n:
            return (x2n,y2n)
        else :
            return (x1o,y1o)
    elif dist(x1o,y1o,x1n,y1n) <= dist(x1o,y1o,x2n,y2n):
        if x1o*(1+per) > x1n and x1o*(1-per) < x1n and y1o*(1+per) > y1n and y1o*(1-per) < y1n:
            return (x1n,y1n)
        else :
            return (x1o,y1o)

cap = cv2.VideoCapture('sentry3.mkv')
ret, frame1 = cap.read()
ret, frame2 = cap.read()
count = 0
while cap.isOpened():
    try:
        diff = cv2.absdiff(frame1,frame2)
    except:
        break
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations=3)
    contours,heirarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=cv2.contourArea,reverse=True)[0:2]
    m2 = cv2.moments(contours[1])
    a,b,c,d = cv2.boundingRect(contours[1])
    x2_n = a+c/2
    y2_n = b+d/2
    m1 = cv2.moments(contours[0])
    a,b,c,d = cv2.boundingRect(contours[0])
    x1_n = a+c/2
    y1_n = b+d/2
    if count == 0 :
        x1_o,x2_o,y1_o,y2_o = x1_n,x2_n,y1_n,y2_n
        count += 1
    else :
        (x1_o,y1_o),(x2_o,y2_o) = mind(x1_o,y1_o,x1_n,y1_n,x2_n,y2_n),mind(x2_o,y2_o,x1_n,y1_n,x2_n,y2_n)
        #print('x1_o=',x1_o,'y1_o=',y1_o,'x2_o=',x2_o,'y2_o=',y2_o,'x1_n=',x1_n,'y1_n=',y1_n,'x2_n=',x2_n,'y2_n=',y2_n)
        if x1_o == x2_o and y1_o == y2_o:
            print()
    #cv2.circle(frame1, (x2_o, y2_o), 5, (0, 0, 255), -1)
    for cnt in (contours):
        (x,y,w,h) = cv2.boundingRect(cnt)

        if cv2.contourArea(cnt) < 3000 :
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1, 'bot 1', (int(x1_o), int(y1_o)+100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        cv2.putText(frame1, 'bot 2', (int(x2_o), int(y2_o)+100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow('feed',frame1)
    frame1 = frame2
    ret,frame2 = cap.read()
    if cv2.waitKey(42) == 27:
        break
cv2.destroyAllWindows()
import cv2
import numpy as np
import math
import serial




def avg_background(roi):
    global r
    cv2.accumulateWeighted(roi,r,0.5)

def segment(roi):
    global r
    bg=r.copy()
    bg=bg.astype("uint8")
    bg=cv2.GaussianBlur(bg,(7,7),0)
    roi = cv2.GaussianBlur(roi, (7,7), 0)



    diff=cv2.absdiff(roi,bg)

    diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    _,diff=cv2.threshold(diff,25,255,cv2.THRESH_BINARY)
    diff=cv2.dilate(diff,np.array([7,7],np.uint8),iterations=20)

    contours,_=cv2.findContours(diff,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    return contours

def controller(img,con,roi):
    global x,y
    hull = max(con, key=cv2.contourArea)

    #left = tuple(hull[hull[:, :, 0].argmin()][0])
    #bottom = tuple(hull[hull[:, :, 1].argmax()][0])
    top = tuple(hull[hull[:, :, 1].argmin()][0])
    #right = tuple(hull[hull[:, :, 0].argmax()][0])



    img = cv2.circle(img, (x+top[0],y+top[1]), 25, (217,159,15), 5)
    img = cv2.circle(img, (x+top[0],y+top[1]), 40, (255, 255, 255),10)
    img = cv2.circle(img, (x + top[0], y + top[1]), 55, (217, 159, 15), 5)
    #img = cv2.circle(img, (x + top[0], y + top[1]), 5, (255, 255, 255), 2)
    #img[y:y+h,x:x+w,:]=cv2.addWeighted(img[y:y+h,x:x+w,:],0.5,roi,0.5,0)
    #img = cv2.line(img, (x+w//2,y+h//2), (x+top[0],y+top[1]), (0, 0, 255), 3)

    return img,top

def directions(roi,top,img):
    global w,h#,ser
    X=top[0]-w/2
    Y=h/2-top[1]
    theta=math.atan(abs(Y)/abs(X))
    theta=math.degrees(theta)
    if(theta<=45 and X>0):

        img = cv2.putText(img, "RIGHT", (80, 130), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
        #ser.write("RIGHT\n".encode())
    if (theta <= 45 and X < 0):

        img = cv2.putText(img, "LEFT", (80, 130), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
        #ser.write("LEFT\n".encode())
    if(45<theta<=90 and Y>0):

        img = cv2.putText(img, "FORWARD", (80, 130), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
        #ser.write("FORWARD\n".encode())
    if(45<theta<=90 and Y<0):

        img = cv2.putText(img, "BACKWARD", (80, 130), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
        #ser.write("BACKWARD\n".encode())
    return img


def pwm(top):
    global w,h
    x1,y1=top[0],top[1]
    x0,y0=w//2,h//2
    length=int(math.sqrt(math.pow(x0-x1,2)+math.pow(y0-y1,2)))
    pwm=int(2.1*length)
    if(pwm>255):
        pwm=255
    print(pwm)






#ser=serial.Serial("COM7",9600,timeout=1)
cap=cv2.VideoCapture(0)
_,f=cap.read()
f=cv2.flip(f,1)
x,y,w,h=320,115,250,250
r=f[y:y+h,x:x+w,:].astype("float")
no_of_frames=0
z=1
while(z):
    ret,frame=cap.read()
    img=cv2.flip(frame,1)
    roi = img[y:y+h,x:x+w,:].copy()
    img = cv2.circle(img, (x + w // 2, y + h // 2), h//2-10, (217,159,15), 3)
    img = cv2.circle(img, (x + w // 2, y + h // 2), h // 2, (255, 255, 255), 10)
    img = cv2.circle(img, (x + w // 2, y + h // 2), h // 2+10, (217,159,15), 3)
    if(no_of_frames<=60):

        avg_background(roi)
        img=cv2.putText(img,"GETTING READY",(80,130),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5,cv2.LINE_AA)

        cv2.imshow("j", img)
    else:
        con=segment(roi)

        #img = cv2.circle(img, (x + w // 2, y + h // 2), 5, (255, 255, 255), 5)
        if(len(con)!=0):
            img,top=controller(img,con,roi)
            img=directions(roi,top,img)
            pwm(top)

            cv2.imshow("j", img)
        else:
            img = cv2.circle(img, (x + w // 2, y + h // 2), 25, (217, 159, 15), 5)
            img = cv2.circle(img, (x + w // 2, y + h // 2), 40, (255, 255, 255), 10)
            img = cv2.circle(img, (x + w // 2, y + h // 2), 55, (217, 159, 15), 5)


            cv2.imshow("j",img)
    no_of_frames+=1
    if(cv2.waitKey(5)==ord("q")):
        z=0
cap.release()
cv2.destroyAllWindows()
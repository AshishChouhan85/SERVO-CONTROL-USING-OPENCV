import cv2
import numpy as np
import math
import serial

####################### FUNCTION TO EXTRACT THE BACKGROUND ######################################################

def avg_background(roi):
    global r                               #INITIAL BACKGROUND SELECTED
    roi=roi.astype("float64")                #ROI CONVERTED TO FLOAT TYPE BECAUSE MULTIPLYING WITH 0.5 NEEDS FLOAT DATA
    cv2.accumulateWeighted(roi,r,0.5)      #50% OF ROI AND 50% OF r IS OVERWRITTEN IN r (60 FRAMES TAKEN)

####################### FUNCTION TO DIFFERENTIATE BETWEEN BACKGROUND AND FOREGROUND AND TO FIND CONTOURS OF HAND##

def segment(roi):
    global r                                                               #AVERAGED BACKGROUND
    bg=r.copy()                                                            #MAKING COPY OF BACKGROUND
    bg=cv2.convertScaleAbs(bg)                                             #CONVERTING BACKGROUND TO INTEGER DATATYPE
    bg=cv2.GaussianBlur(bg,(7,7),0)                                        #APPLYING BLUR SO THAT SOME EDGES ARE REMOVED
    roi = cv2.GaussianBlur(roi, (7,7), 0)
    diff=cv2.absdiff(roi,bg)                                               #GETTING OUR HAND ONLY
    diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    _,diff=cv2.threshold(diff,25,255,cv2.THRESH_BINARY)
    diff=cv2.dilate(diff,np.array([7,7],np.uint8),iterations=20)
    contours,_=cv2.findContours(diff,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.imshow("n",diff)
    return contours

####################### FUNCTION TO DRAW CIRCLE ON FINGERTIP AND CONTROLLER BODY #############################

def controller(img,contour):
    global x,y
    hand_outline = max(contour, key=cv2.contourArea)                              #GETTING CONTOUR WITH LARGEST AREA WHICH IS OUR HAND IN MOST CASES
    top = tuple(hand_outline[hand_outline[:, :, 1].argmin()][0])                      #GETTING COORDINATE OF TOPMOST POINT OF HAND

    img = cv2.circle(img, (x+top[0],y+top[1]), 25, (0,0,255), 5)      #217,159,15
    img = cv2.circle(img, (x+top[0],y+top[1]), 40, (255, 255, 255),10)
    img = cv2.circle(img, (x + top[0], y + top[1]), 55, (0,0,255), 5)

    return img,top

######################### FUNCTION TO CALCULATE DIRECTIONS ##################################################

def directions(top,img):
    global w,h
    X=top[0]-w/2                               #CALCULATING HORIZONTAL DISTANCE OF FINFERTIP FROM CENTRE OF CIRCLE
    Y=h/2-top[1]                               #CALCULATING VERTICAL DISTANCE OF FINFERTIP FROM CENTRE OF CIRCLE
    if (X==0):
        theta=90
    else:
        theta=math.atan(abs(Y)/abs(X))         #CALCULATING ANGLE OF THE VECTOR
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

############################ FUNCTION TO CALCULATE ANGLE OF SERVO ##############################################

def servo_angle(top,img):
    x=top[0]
    y=top[1]
    angle_x=int((-0.48)*x+150)
    angle_y=int((-0.48)*y+150)
    #print(angle_x,angle_y)
    #img = cv2.putText(img, str((angle_x,angle_y)), (30, 130), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
    text1 = str(angle_x) + "#"
    text2 = str(angle_y) + "$"
    ser.write(text1.encode())
    ser.write(text2.encode())
    return img

############################ FUNCTION TO CALCULATE VALUE OF PWM ################################################

def pwm(top):
    global w,h
    x1,y1=top[0],top[1]
    x0,y0=w//2,h//2
    length=int(math.sqrt(math.pow(x0-x1,2)+math.pow(y0-y1,2))) #DISTANCE FORMULA
    pwm=int(2.1*length)                                        #CALCULATION OF PWM
    if(pwm>255):
        pwm=255

############################ FUNCTION TO GIVE BLENDING EFFECT TO CONTROLLER ####################################

def blending(img):
    global x,y,w,h,pad
    controller_bg_drawn=img[y-pad:y+h+pad,x-pad:x+w+pad,:].copy()
    blended_img=cv2.addWeighted(controller_bg,0.5,controller_bg_drawn,0.5,0)
    img[y - pad:y + h + pad, x - pad:x + w + pad, :]=blended_img.copy()
    return img


ser=serial.Serial("COM7",9600,timeout=1)
cap=cv2.VideoCapture(0)
_,f=cap.read()
f=cv2.flip(f,1)
x,y,w,h,pad=320,115,250,250,100
r=f[y:y+h,x:x+w,:].astype("float")              #FIRST BACKGROUND CREATED,WILL BE USED IN AVERAGING AND LATER WILL BECOME THE AVG BACKGROUND
print(type(r))
no_of_frames=0                                  #60 FRAMES WILL WE TAKEN TO AVERAGE BACKGROUND
z=1
while(z):
    ret,frame=cap.read()
    img=cv2.flip(frame,1)                                   #FLIPPING IS DONE SO THAT THERE IS NO CONFUSION IN CONTROL
    roi = img[y:y+h,x:x+w,:].copy()                         #REAL ROI
    controller_bg=img[y-pad:y+h+pad,x-pad:x+w+pad,:].copy() #FAKE ROI,REAL ROI IS INSIDE


    if(no_of_frames<=60):   #HERE BACKGROUND IS MADE

        avg_background(roi)
        img=cv2.putText(img,"GETTING READY",(80,130),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5,cv2.LINE_AA)


    else:                   #AFTER BACKGROUND IS MADE WE GET CONTOURS HERE
        contour=segment(roi)
        img = cv2.circle(img, (x + w // 2, y + h // 2), h // 2 - 10, (0,0,255), 3)
        img = cv2.circle(img, (x + w // 2, y + h // 2), h // 2, (255, 255, 255), 10)
        img = cv2.circle(img, (x + w // 2, y + h // 2), h // 2 + 10, (0,0,255), 3)     #CONTROLLER BODY IS CREATED


        if(len(contour)!=0):    #IF CONTOURS ARE DETECTED
            img,top=controller(img,contour)
            img=blending(img)
            img=servo_angle(top,img)
            #img=directions(top,img)
            #pwm(top)



        else:               #IF CONTOURS ARE NOT DETECTED
            img = cv2.circle(img, (x + w // 2, y + h // 2), 25, (0,0,255), 5)
            img = cv2.circle(img, (x + w // 2, y + h // 2), 40, (255, 255, 255), 10)
            img = cv2.circle(img, (x + w // 2, y + h // 2), 55, (0,0,255), 5)          #CONTROLLER CIRCLE IS ALWAYS IN MIDDLE IF NO CONTOUR IS DETECTED
            img = blending(img)


    cv2.imshow("j",img)
    no_of_frames+=1                    #NO. OF FRAMES IS INCREMENTED
    if(cv2.waitKey(1)==ord("q")):
        text1 = "90#"
        text2 = "90$"
        ser.write(text1.encode())
        ser.write(text2.encode())
        z=0
cap.release()
cv2.destroyAllWindows()
# GESTURE-CONTROLLED-BOT-VIRTUAL-CONTROLLER

# INTRODUCTION
This is the code for making a virtual controller which can be controlled by moving our fingertip in upward,downward,left and right direction.
This project has been made using Opencv library in python. Although the controller has been made to control a 4 wheeled robot,it can be used to control variety 
of things which depends upon user's imagination.

# LOGIC BEHIND THIS PROJECT
The project uses methods like background removal, blurring and thresholding the ROI to a binary image so that contours can be detected.
After detecting the largest contour(which is the contour of our hand),the topmost point of the contour (which is generally the fingertip) is detected.<br>
The larger circle around the ROI has been divided into four parts of equal area using basic trigonometry for up,down,left and right direction.Currently virtual controller 
can control any bot (with minute change in code) along x and y axis, but it can be extended to z axis by also considering the area of contour detected.




# PROBLEMS AND FURTHER SCOPE OF IMPROVEMENTS
Contours of the hand can be detected only when camera is stationary and background is still. Also too much objects in the background makes the hand difficult to detect.
All these errors can be rectified using a deep learning model which can detect hand with maximum accuracy.

# VIDEO
[CLICK HERE](https://drive.google.com/file/d/17wxnTURtqnJqas1tKpgifAKJcFCUi-dO/view?usp=sharing)



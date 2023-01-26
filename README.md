# SERVO CONTROL USING OPENCV

# INTRODUCTION
This is the code for making a virtual controller which can be controlled by moving our fingertip in upward,downward,left and right direction.
This project has been made using Opencv library in python. Although the controller has been made to control a 4 wheeled robot,it can be used to control variety 
of things which depends upon user's imagination.

# LOGIC BEHIND THIS PROJECT
The project uses methods like background removal, blurring and thresholding the ROI to a binary image so that contours can be detected.
After detecting the largest contour(which is the contour of our hand),the topmost point of the contour (which is generally the fingertip) is detected.<br>
The larger circle around the ROI has been divided into four parts of equal area using basic trigonometry for up,down,left and right direction.Currently virtual controller 
can control any bot (with minute change in code) along x and y axis, but it can be extended to z axis by also considering the area of contour detected.<br>
# Background
A background is created at the start by averaging the first 60 frames.<br>
![background](https://github.com/AshishChouhan85/GESTURE-CONTROLLED-BOT-VIRTUAL-CONTROLLER/blob/master/Images/background.png)<br>
<br>
# Hand
![hand](https://github.com/AshishChouhan85/GESTURE-CONTROLLED-BOT-VIRTUAL-CONTROLLER/blob/master/Images/hand.png)<br>
<br>
# Thresholded hand
The background is subtracted from the current image and thresholded to get this image.<br>
![threshold](https://github.com/AshishChouhan85/GESTURE-CONTROLLED-BOT-VIRTUAL-CONTROLLER/blob/master/Images/threshold.png)<br>
<br>
# Dilated hand
Finally the above image is dilated so that a perfect contour of the hand is detected.<br>
![dilate](https://github.com/AshishChouhan85/GESTURE-CONTROLLED-BOT-VIRTUAL-CONTROLLER/blob/master/Images/dilate.png)<br>




# PROBLEMS AND FURTHER SCOPE OF IMPROVEMENTS
Contours of the hand can be detected only when camera is stationary and background is still. Also too much objects in the background makes the hand difficult to detect.
All these errors can be rectified using a deep learning model which can detect hand with maximum accuracy.

# VIDEO
[CLICK HERE](https://drive.google.com/file/d/17wxnTURtqnJqas1tKpgifAKJcFCUi-dO/view?usp=sharing)



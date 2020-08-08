# GESTURE-CONTROLLED-BOT-VIRTUAL-CONTROLLER

# INTRODUCTION
This is the code for making a virtual controller which can be controlled by moving our fingertip in upward,downward,left and right direction.
This project has been made using Opencv library in python. Although the controller has been made to control a 4 wheeled robot,it can be used to control variety 
of things which depends upon user's imagination.

# LOGIC BEHIND THIS PROJECT
The project uses methods like background removal, blurring and thresholding the ROI to a binary image so that contours can be detected.
After detecting the largest contour(which is the contour of our hand), convex hull method is used to detect the fingertips of the hand.From those coordinates of the fingertips,
the coordinates of the topmost fingertip is taken around which a circle is made.<br>
The larger circle around the ROI has been divided into four parts of equal area using basic trigonometry for up,down,left and right direction.

# PROBLEMS AND FURTHER SCOPE OF IMPROVEMENTS
Contours of the hand can be detected only when camera is stationary and background is still. Also too much objects in the background makes the hand difficult to detect.
All these errors can be rectified using a deep learning model which can detect hands with maximum accuracy.

# VIDEO
[CLICK HERE](https://drive.google.com/file/d/12bfXmal6n2OYjdiwFV9Zqgh01aCjUmKK/view?usp=sharing)



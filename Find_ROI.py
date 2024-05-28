import pytesseract as tess
import os
import cv2
import re
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

path = filedialog.askopenfilename()
# path ='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/Archive/GBR_VERSTAPPEN_L1.mov'
# print(path)

img = cv2.VideoCapture(path) 
success, image = img.read()
ret, currentFrame = img.read()

frame= 2


# while success:


# 	### Get Frame

# 	img.set(1, frame)
# 	success, image = img.read()
# 	ret, currentFrame = img.read()
# 	cv2.imshow('Frame' ,currentFrame)
# 	cv2.waitKey(0)
# 	frame+=1
# 	# cv2.destroyAllWindows()

# Speed = currentFrame[82:139, 152:180]
# # cv2.imshow('1', Speed)
# cv2.waitKey(0)
# while True:

# 	img.set(1, frame)
# 	success, image = img.read()
# 	ret, currentFrame = img.read()

# 	cv2.imshow('Frame', currentFrame)
# 	cv2.waitKey(0)

# 	print(frame)

# 	frame+=1




# Track = currentFrame[377:402, 409:462]
# cv2.imshow('Frame' ,currentFrame)
# cv2.imshow('1', Track)
# cv2.waitKey(0)
cv2.destroyAllWindows()
ROIs=cv2.selectROIs("Test", currentFrame)




Track = currentFrame[ROIs[0][1]:ROIs[0][1]+ROIs[0][3], ROIs[0][0]:ROIs[0][0]+ROIs[0][2]]
print('Track: '+str(ROIs[0][1])+':'+str(ROIs[0][1]+ROIs[0][3])+', '+str(ROIs[0][0])+':'+str(ROIs[0][0]+ROIs[0][2]))

Name = currentFrame[ROIs[1][1]:ROIs[1][1]+ROIs[1][3], ROIs[1][0]:ROIs[1][0]+ROIs[1][2]]
print('Name: '+str(ROIs[1][1])+':'+str(ROIs[1][1]+ROIs[1][3])+', '+str(ROIs[1][0])+':'+str(ROIs[1][0]+ROIs[1][2]))

Speed = currentFrame[ROIs[2][1]:ROIs[2][1]+ROIs[2][3], ROIs[2][0]:ROIs[2][0]+ROIs[2][2]]
print('Speed: '+str(ROIs[2][1])+':'+str(ROIs[2][1]+ROIs[2][3])+', '+str(ROIs[2][0])+':'+str(ROIs[2][0]+ROIs[2][2]))

Sec1 = currentFrame[ROIs[3][1]:ROIs[3][1]+ROIs[0][3], ROIs[3][0]:ROIs[3][0]+ROIs[3][2]]
print('S1: '+str(ROIs[3][1])+':'+str(ROIs[3][1]+ROIs[3][3])+', '+str(ROIs[3][0])+':'+str(ROIs[3][0]+ROIs[3][2]))

Sec2 = currentFrame[ROIs[4][1]:ROIs[4][1]+ROIs[1][3], ROIs[4][0]:ROIs[4][0]+ROIs[4][2]]
print('S2: '+str(ROIs[4][1])+':'+str(ROIs[4][1]+ROIs[4][3])+', '+str(ROIs[4][0])+':'+str(ROIs[4][0]+ROIs[4][2]))

Sec3 = currentFrame[ROIs[5][1]:ROIs[5][1]+ROIs[2][3], ROIs[5][0]:ROIs[5][0]+ROIs[5][2]]
print('S3: '+str(ROIs[5][1])+':'+str(ROIs[5][1]+ROIs[5][3])+', '+str(ROIs[5][0])+':'+str(ROIs[5][0]+ROIs[5][2]))

Lap = currentFrame[ROIs[6][1]:ROIs[6][1]+ROIs[2][3], ROIs[6][0]:ROIs[6][0]+ROIs[6][2]]
print('Lap: '+str(ROIs[6][1])+':'+str(ROIs[6][1]+ROIs[6][3])+', '+str(ROIs[6][0])+':'+str(ROIs[6][0]+ROIs[6][2]))



cv2.imshow('1', Track)
cv2.imshow('2', Name)
cv2.imshow('3', Speed)
cv2.imshow('4', Sec1)
cv2.imshow('5', Sec2)
cv2.imshow('6', Sec3)
cv2.imshow('7', Lap)



cv2.waitKey(0)
cv2.destroyAllWindows()

### Quali AUT
		# roi_track = currentFrame[11:48, 12:81]

		# roi_name1 = currentFrame[127:157, 260:392]
		
		# roi_speed1 = currentFrame[329:357, 402:470] 

		# roi_sec1_1 =currentFrame[555:560, 300:370]
		# roi_sec2_1 =currentFrame[555:560, 400:470]
		# roi_sec3_1 =currentFrame[555:560, 500:570]

		# roi_lap1 = currentFrame[1247:1278, 1271:1307]



### Quali AUT D2
		# Track: 15:46, 13:81
		# Name: 772:809, 258:423
		# Speed: 976:1010, 400:473
		# S1: 1206:1212, 312:356
		# S2: 1208:1212, 407:448
		# S3: 1207:1213, 507:539
		# Lap: 1248:1277, 1271:1311

		# roi_lap1 = currentFrame[1258:1295, 1275:1377]


### Race FRA D1	
		# roi_track = currentFrame[21:42, 16:76]

		# roi_name1 = currentFrame[130:157, 259:480]
		
		# roi_speed1 = currentFrame[343:367, 404:469] 

		# roi_sec1_1 =currentFrame[555:560, 300:370]
		# roi_sec2_1 =currentFrame[555:560, 400:470]
		# roi_sec3_1 =currentFrame[555:560, 500:570]

		# roi_lap1 = currentFrame[1258:1295, 1275:1377]


### Race FRA D2
		# roi_name2 = currentFrame[772:809, 258:440]
		
		# roi_speed1 = currentFrame[993:1019, 409:465] 

		# roi_sec1_1 =currentFrame[1206:1212, 312:356]
		# roi_sec2_1 =currentFrame[1208:1212, 407:448]
		# roi_sec3_1 =currentFrame[1207:1213, 507:539]



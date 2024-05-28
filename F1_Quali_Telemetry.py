#https://www.formula1.com/en/f1-live.html

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import csv

import pytesseract as tess

import os
import cv2
import re
import time

import tkinter as tk
from tkinter import filedialog

import Rename_Video_File 


def OCR_QUALI_TELEMETRICS_IPAD(path, Frame_Skipped, filename):

	a = time.time()
	## Creation of DF


	Headers1=['Frame','Driver','Speed', 'Sector', 'Lap','Lap Time', 'T_Delta']
	CSV1 = pd.DataFrame(columns=Headers1)



	root = tk.Tk()
	root.withdraw()

	# path = filedialog.askopenfilename()


	img = cv2.VideoCapture(path)
	fps = img. get(cv2. CAP_PROP_FPS) 
	success, image = img.read()

	Digit_Config = '--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'

	Lap_Config = r'--oem 3 tessedit_char_whitelist=0123456789/ --psm 13'



	BG = np.sum(np.array([57, 56, 64]))
	BG1 = np.sum(np.array([55, 50, 75]))


	length = int(img.get(cv2.CAP_PROP_FRAME_COUNT))

	frame = 0
	Stopper1 = False
	S1_1_test = False
	S3_1_test = False


	End_Shesh = False
	End_Shesh_Count = 0


	## 1st Frame Selection (Names, Track)
	img.set(1, frame)
	success, image = img.read()
	ret, currentFrame = img.read()


	try:
		roi_track = currentFrame[16:43, 14:83]

		roi_name1 = currentFrame[128:156, 261:478]

		roi_Q = currentFrame[1249:1275, 1267:1311]
	except:
		pass

	# cv2.imshow('Track', roi_track)
	# cv2.imshow('name', roi_name1)
	# cv2.imshow('Sesh', roi_Q)

	# cv2.waitKey()
	roi_name1 = cv2.blur(roi_name1, (2, 2))
	roi_name1 = cv2.cvtColor(roi_name1, cv2.COLOR_BGR2GRAY)
	(thresh, roi_name1) = cv2.threshold(roi_name1, 127, 255, cv2.THRESH_BINARY)
	roi_name1 = cv2.blur(roi_name1, (2, 2))

	Name1 = tess.image_to_string(roi_name1, lang='eng', config='--psm 6')
	Name1 = re.sub('',"", Name1)
	Name1 = re.sub('\n',"", Name1)
	Name1 = re.sub('2',"Z", Name1)



	roi_track = cv2.blur(roi_track, (2, 2))
	roi_track = cv2.cvtColor(roi_track, cv2.COLOR_BGR2GRAY)
	(thresh, roi_track) = cv2.threshold(roi_track,  185, 255, cv2.THRESH_BINARY)
	roi_track = cv2.blur(roi_track, (2, 2))


	# cv2.imshow('Track', roi_track)
	# cv2.waitKey()
	# cv2.destroyAllWindows()
	# cv2.waitKey()


	Track = tess.image_to_string(roi_track, config='--psm 6')
	Track = re.sub('',"", Track)
	Track = re.sub('\n',"", Track)



	### Q
	roi_Q = cv2.cvtColor(roi_Q, cv2.COLOR_BGR2GRAY)


	Qnum = tess.image_to_string(roi_Q, config='--psm 6')
	Qnum = re.sub('',"", Qnum)
	Qnum = re.sub('\n',"", Qnum)
	Qnum = re.sub('i',"1", Qnum)


	# cv2.imshow('Track', roi_track)
	# cv2.imshow('name', roi_name1)
	# cv2.imshow('Sesh', roi_Q)

	# cv2.waitKey()
	print("Quali sesh:",Track,Name1,Qnum)



	Starting_Time = time.time()

	n_S1 = 0
	n_S2 = 0
	n_S3 = 0

	while success:


		### Get Frame

		img.set(1, frame)
		success, image = img.read()
		ret, currentFrame = img.read()

		if frame%60 == 0:
			T_Now = time.time()
			Frame_Now = frame


		try:
			ETA = (length-frame)*((time.time() - T_Now)/(frame-Frame_Now))
			print(' Processing frame: ', frame,' of ',length,' (',round(100*frame/length,1),'%)',' ETA: ',round(ETA/60,1) , ' min.')
		except:
			pass
		
		### Check for session ending

		try:
			roi_END = currentFrame[107:137, 555:624]
		except:
			break

		END= np.sum(np.around(np.mean(roi_END, axis=(0,1)),decimals=0))



		if END > 100: ## In Sesh

			try:

			#Driver 1

				roi_speed1 = currentFrame[327:360, 404:467] 

				# roi_sec1_1 =currentFrame[556:560, 314:356]
				# roi_sec2_1 =currentFrame[560:564, 403:452]
				roi_sec3_1 =currentFrame[553:561, 508:534]



			except:
				pass
		if END < 100: ## End of Sesh
			End_Shesh = True
			End_Shesh_Count+=1
			# print(End_Shesh_Count)

			try:

			#Driver 1

				roi_speed1 = currentFrame[327:360, 404:467] 

				# roi_sec1_1 =currentFrame[589:595, 330:350]
				# roi_sec2_1 =currentFrame[591:595, 512:535]
				roi_sec3_1 =currentFrame[553:561, 508:534]

			except:
				pass

		##Sectors Driver 1

		# sec1col_1= np.around(np.mean(roi_sec1_1, axis=(0,1)),decimals=0)
		# sec2col_1= np.around(np.mean(roi_sec2_1, axis=(0,1)),decimals=0)
		sec3col_1= np.around(np.mean(roi_sec3_1, axis=(0,1)),decimals=0)

		
		#print(type(np.sum(sec3col)),type(BG))
		if (End_Shesh == False) or (End_Shesh == True and End_Shesh_Count > 6/Frame_Skipped):
		

			if ( ( BG * 1.10 < np.sum(sec3col_1) ) and frame <= 0.2 * length):
				#print("\nSector 1"
				S1_1_test=True

			elif ( ( BG * 1.10 < np.sum(sec3col_1) ) and frame >= 0.8 * length):
				S1_1_test=False
				



			### Sector Test for Sequence Driver 1

			# if (Sector_1 == "Sector 1" and Stopper1 == False and n_S1 > 3) :
			# 	S1_1_test=True
			# 	S3_1_test=False
				


			# if Sector_1 == 'Sector 3' and S1_1_test == True and n_S3 > 3:
			# 	S1_1_test = False
			# 	S3_1_test = True
			# 	Stopper1 = True

			# if Sector_1 == 'Sector 1' and S3_1_test == True and n_S1 > 3:
			# 	S1_1_test = False
			# 	S3_1_test = False



			
			# S1_1_test = True
			### DF log & speed for driver 1
			if S1_1_test == True :
			## Speed Driver 1
				try:
					roi_speed1 = cv2.blur(roi_speed1, (3, 3))
					roi_speed1 = cv2.cvtColor(roi_speed1, cv2.COLOR_BGR2GRAY)
					(thresh, roi_speed1) = cv2.threshold(roi_speed1, 185, 255, cv2.THRESH_BINARY)
					roi_speed1 = cv2.blur(roi_speed1, (2, 2))


					Speed1 = tess.image_to_string(roi_speed1, lang='script/F1r', config='--psm 6')
					Speed1 = int(re.sub("[^0-9]", "", Speed1))
					
				except:
					Speed1 = ""

		 
				### Print result
				print(Track+': '+Name1+' at '+str(Speed1)+' kph on frame: '+str(frame)+' for '+ str(S1_1_test) +' during '+Qnum+'\n')


				# cv2.imshow('Frame', currentFrame)
				# cv2.imshow('speed', roi_speed1)
				# # cv2.imshow('S1', roi_sec1_1)
				# # cv2.imshow('S2', roi_sec2_1)
				# cv2.imshow('S3', roi_sec3_1)

				# cv2.waitKey()

				### Log in DFs
				if (End_Shesh == False) or (End_Shesh == True and End_Shesh_Count > 6/Frame_Skipped):
					CSV1_While = pd.DataFrame([{'Frame':frame,'Driver':Name1, 'Speed':Speed1, 'Lap': Qnum, 'T_Delta': Frame_Skipped/fps}], columns=Headers1)

					CSV1 = CSV1.append(CSV1_While)

				else:
					CSV1_While = pd.DataFrame([{'Frame':frame,'Driver':Name1, 'Speed':"", 'Lap': Qnum, 'T_Delta': Frame_Skipped/fps}], columns=Headers1)

					CSV1 = CSV1.append(CSV1_While)





		Speed1 = ''
		frame = frame+ Frame_Skipped

		c = time.time()
		### While end



	### Get last lap time
	img.set(1, frame - Frame_Skipped)
	ret, currentFrame = img.read()
	if END > 100:
		roi_lastlap_1 = currentFrame[235:255, 587:673]
	if END < 100:							## End of Sesh
		roi_lastlap_1 = currentFrame[291:309, 584:677]



	roi_lastlap_1 = cv2.cvtColor(roi_lastlap_1, cv2.COLOR_BGR2GRAY)
	# (thresh, roi_lastlap_1) = cv2.threshold(roi_lastlap_1, 100, 255, cv2.THRESH_BINARY_INV)
	
	lastlap_1 = tess.image_to_string(roi_lastlap_1, lang='eng', config='--psm 6')
	lastlap_1 = re.sub('',"", lastlap_1)
	lastlap_1 = re.sub('\n',"", lastlap_1)
	print(lastlap_1)
	CSV1['Lap Time']=lastlap_1


	

	CSV1.to_csv("Output/Quali/"+Track+'_'+Qnum+'_'+Name1+'.csv',index=True)


	print('##############################################################')
	print(filename,' took ',round((time.time()-a)/60,2),' min.')
	print('##############################################################')



def File_Processing():

	directory='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali'
	ArchiveDir ='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/Archive'


	for filename in os.listdir(directory):
	    if filename.endswith(".mp4") or filename.endswith(".MP4") or filename.endswith(".mov"):


	    	current_path=os.path.join(directory, filename)

	    	print(current_path)

	    	

	    	OCR_QUALI_TELEMETRICS_IPAD(current_path, 1, filename)
	    	

	    	time.sleep(3)

	    	os.rename((os.path.join(directory, filename)),(os.path.join(ArchiveDir, filename)))

	  
	    else:
	    	continue






while True:
	print('Settings are currently for HUN GP.')
	print('Looking for Video!')
	Rename_Video_File.LoopThru()
	File_Processing()
	time.sleep(3)






#OCR_RACE_TELEMETRICS_IPAD('Input/Archive/AUT_LEC_RIC_L25.MP4',10,'TEST_TIME')

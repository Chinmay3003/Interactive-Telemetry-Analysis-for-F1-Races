import numpy as np
import pandas as pd

import re

import os 

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import tkinter as tk
from tkinter import filedialog



def Choose_File():
	directory='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Output/Quali/'
	ArchiveDir ='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/Archive'	
	
	File_List =[]

	for filename in os.listdir(directory):
		if filename.endswith(".csv"):
			filename = re.sub(".csv", "", filename)

			File_List.append(filename)


			# print(filename.split('_'))

	File_List.sort()
	print('\n')
	for file in File_List: print(file)
	print('\n')

	file1 = input('Choose File #1: ')

	file2 = input('Choose File #2: ')

	return file1+'.csv', file2+'.csv'






def Plot_Data(File1, File2):

	directory = '/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Output/Quali/'



	Path1 = directory+File1

	Path2 = directory+File2

	# Path1s="/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Output/Quali/GBR_L1_HAMILTON.csv"


	pattern = "Quali/(.*?)_"

	Track1 = str(re.search(pattern, Path1).group(1))
	Track2 = str(re.search(pattern, Path2).group(1))



	df1 = pd.read_csv(Path1)
	df2 = pd.read_csv(Path2)

	df1 = df1.interpolate()
	df2 = df2.interpolate()


##### D1

	df1['Distance'] = df1.apply(lambda row: 1000*row.Speed*(row.T_Delta/3600), axis = 1 )
	df1['Cumul_Distance'] = df1['Distance'].cumsum()

	if Track1 =='FRA': 
		Lap_Length =5842
		Track_Full = 'France'
		Sectors = []

	elif Track1 =='AUT': 
		Lap_Length =4318
		Corner_Num = {1:250, 2:750, 3:1200, 4:2000, 5:2300, 6:2550, 7:2900, 8:3150, 9:3640, 10: 3940}
		Track_Full = 'Austria'
		Sectors = [1200, 2875, 4318]
		S1 = Sectors[0]
		S2 = Sectors[1]
		S3 = Sectors[2]

	elif Track1 =='GBR': 
		Lap_Length =5891
		Corner_Num = {'1 & 2':500, '3 & 4':825, 5:1050, 6:1750, 7:2100, 8:2300, 9:2800, '10 - 12': 3650, 13: 4050, 14: 4850, 15: 5100, '16 - 18': 5500}
		Track_Full = 'Great Britain'
		Sectors = [1800, 4250, 5891]
		S1 = Sectors[0]
		S2 = Sectors[1]
		S3 = Sectors[2]

	elif Track1 =='HUN': 
		Lap_Length =4381
		Corner_Num = {1:450, 2:950, 3:1350, 4:1675, 5:1900, 6:2250, 7: 2400, '8 & 9':2650, 10: 2900, 11: 3250, 12: 3600, 13: 3860, 14: 4050}
		Track_Full = 'Hungarian'
		Sectors = [1800, 3300, 4381]
		S1 = Sectors[0]
		S2 = Sectors[1]
		S3 = Sectors[2]

	else:
		print('Track not found.')
		# break


	Driver1=df1['Driver'].values[0]
	ShortName1 = Driver1[0:3]
	try:
		Time1 = df1['Lap Time'].values[0]

		split = Time1.split(':')

		Tm = split[0]

		split = split[1].split('.')

		Ts = split[0]

		Tms = split[1]

		Time_in_S_1 = int(Tm)*60 + int(Ts) + int(Tms)/1000

	except:
		Time_in_S_1 = 1

	Err1 = round(100*(Time_in_S_1-df1['T_Delta'].sum())/Time_in_S_1, 3)
	Err1 = ('%s \nTime: %s\nerr: %s %%' %(Driver1, Time1, Err1))




##### D2


	df2['Distance'] = df2.apply(lambda row: 1000*row.Speed*(row.T_Delta/3600), axis = 1 )
	df2['Cumul_Distance'] = df2['Distance'].cumsum()




	Driver2=df2['Driver'].values[0]
	ShortName2 = Driver2[0:3]
	try:
		Time2 = df2['Lap Time'].values[0]

		split = Time2.split(':')

		Tm = split[0]

		split = split[1].split('.')

		Ts = split[0]

		Tms = split[1]

		Time_in_S_2 = int(Tm)*60 + int(Ts) + int(Tms)/1000
	except:
		Time_in_S_2 = 1

	Err2 = round(100*(Time_in_S_2-df2['T_Delta'].sum())/Time_in_S_2, 3)
	Err2 = ('%s \nTime: %s\nerr: %s %%' %(Driver2 , Time2, Err2))





	Speed_Table1 = df1['Speed'].tolist()
	Cumul_Distance_Table1 = df1['Cumul_Distance'].tolist()

	Speed_Table2 = df2['Speed'].tolist()
	Cumul_Distance_Table2 = df2['Cumul_Distance'].tolist()

	ymin = min(Speed_Table1)
	ymax = max(Speed_Table1)
	xmin = min(Cumul_Distance_Table1)*1.02
	xmax = max(Cumul_Distance_Table1)*0.98
	### Get Time Delta

	df1['Live_Timing'] = df1['T_Delta'].cumsum()
	df2['Live_Timing'] = df2['T_Delta'].cumsum()

	Live_Timing_1 = np.array(df1['Live_Timing'].tolist())

	Live_Timing_2 = np.array(df2['Live_Timing'].tolist())

	Drivers_Delta1= []
	Drivers_Delta2 = []

	for dist in Cumul_Distance_Table1:
		Delta_Time_Dist = np.interp(dist, Cumul_Distance_Table1, Live_Timing_1) - np.interp(dist, Cumul_Distance_Table2, Live_Timing_2)

		Drivers_Delta1.append(-Delta_Time_Dist)


	for dist in Cumul_Distance_Table2:
		Delta_Time_Dist = np.interp(dist, Cumul_Distance_Table1, Live_Timing_1) - np.interp(dist, Cumul_Distance_Table2, Live_Timing_2)

		Drivers_Delta2.append(-Delta_Time_Dist)

	Drivers_Delta = (np.array(Drivers_Delta1) + np.array(Drivers_Delta1))/2

	Title = input('Choose alternative title: ')
	if Title == '':
		Title = "Speed Telemetry\n%s vs %s at %s GP during %s" %(Driver1, Driver2, Track_Full, df1['Lap'].values[0])
	Plot_File_Name = "%s vs %s at %s GP during %s" %(Driver1, Driver2, Track_Full, df1['Lap'].values[0])

	### Zeroing of Plot

	Gap_Between_Driver = df1.loc[df1.Speed == max(Speed_Table1), ['Cumul_Distance']].values[0]- df2.loc[df2.Speed == max(Speed_Table2), ['Cumul_Distance']].values[0]

	Cumul_Distance_Table2 = Cumul_Distance_Table2 +Gap_Between_Driver




#### Plot
	plt.style.use('dark_background')

	fig, ax = plt.subplots()









	ax.plot(Cumul_Distance_Table1, Speed_Table1, marker = '', color='white', label=Err1, alpha = 1)
	#ax[1].plot('cumsum', 'Sector', data=df1, marker = '', color='b')

	ax.plot(Cumul_Distance_Table2, Speed_Table2, linestyle='--', color='r', label=Err2)
	#ax[1].plot('cumsum', 'Sector', data=df2, marker = '', color='grey')

	leg = ax.legend(loc='center', bbox_to_anchor=(.39, .1), fancybox = True, shadow=True, ncol=1, fontsize = 13)
	leg.get_frame().set_alpha(1)


	ax.set_ylim([.75*ymin, 1.20*ymax])
	ax.set_xlim([0,xmax])
	ax.set_xlabel('Distance (m)', fontsize = 14)
	ax.set_ylabel('Speed (kph)', fontsize = 14)
	
	ax.xaxis.set_major_locator(MultipleLocator(250))
	ax.yaxis.set_major_locator(MultipleLocator(25))

	#ax[0].xaxis.set_major_formatter('{x:.0f}')

	#ax[0].xaxis.set_minor_locator(MultipleLocator(50))

	ax.set_title(Title, pad=40, fontsize=26)
	ax.grid(color='m', linestyle='--', linewidth=.5, alpha = .7)
	#ax[1].grid(color='m', linestyle='--', axis='x', linewidth=1)


	ax2 = ax.twinx()

	ax2.plot(Cumul_Distance_Table1, Drivers_Delta, color='y', alpha = .7, linewidth=1)
	ax2.plot(Cumul_Distance_Table1, np.array(Cumul_Distance_Table1)*0, linestyle='--', color='y', alpha = .4, linewidth=1)

	ax2.set_ylabel('Delta (s)', fontsize = 14, color = 'y', alpha = .7)
	m = max( abs(min(Drivers_Delta)), abs(max(Drivers_Delta)) )
	ax2.set_ylim(-2*m, 2*m)  

	ax2.spines['right'].set(color = 'y', alpha = 0.7)

	ax2.tick_params(axis='y', labelcolor='y')

	ax2.text( xmax + 180, m, ShortName1+'\nAhead', color = 'black', alpha = .9, horizontalalignment='center', verticalalignment='center', fontsize=14, bbox=dict(facecolor='y', alpha=0.5))
	ax2.text( xmax + 180, -m, ShortName2+'\nAhead', color = 'black', alpha = .9, horizontalalignment='center', verticalalignment='center', fontsize=14, bbox=dict(facecolor='y', alpha=0.5))




	for Num in Corner_Num:
		ax.text(Corner_Num[Num],ax.get_ylim()[1]+4, Num, horizontalalignment='center', verticalalignment='center', fontsize=13, bbox=dict(facecolor='red', alpha=0.5))
		# ax.axvline(Corner_Num[Num], color='black', linestyle='--', linewidth=.6)

		Speed_Delta = np.interp(Corner_Num[Num], Cumul_Distance_Table1, Speed_Table1) - np.interp(Corner_Num[Num], Cumul_Distance_Table2, Speed_Table2)
		
		if Speed_Delta >=0:
			faster = ShortName1
		else:
			faster = ShortName2


		Speed_Delta = faster  + '\n' + str(round(abs(Speed_Delta),2))+'\nkph'

		ax.text(Corner_Num[Num], ax.get_ylim()[1]-29, Speed_Delta, horizontalalignment='center', verticalalignment='center', fontsize=13, bbox=dict(facecolor='red', alpha=.5))

		ax.annotate('', xytext = (Corner_Num[Num], ax.get_ylim()[1]-35), xy = (Corner_Num[Num], np.interp(Corner_Num[Num], Cumul_Distance_Table1, Speed_Table1)), arrowprops = {'arrowstyle': '-|>', 'linestyle':'--', 'color': 'gray'})

	print(S1, S2, S3)

	ax.axvline(S1, color='white', linestyle='-.', linewidth= 1, alpha = .6)
	ax.text((0+S1)/2, ax.get_ylim()[0]+10, "Sector 1", horizontalalignment='center', verticalalignment='center', fontsize=16, bbox=dict(facecolor='green', alpha=0.5))

	ax.axvline(S2, color='white', linestyle='-.', linewidth=1, alpha = .6)
	ax.text((S1+S2)/2,ax.get_ylim()[0]+10, "Sector 2", horizontalalignment='center', verticalalignment='center', fontsize=16, bbox=dict(facecolor='green', alpha=0.5))

	ax.axvline(S3, color='white', linestyle='-.', linewidth=1, alpha = .6)
	ax.text((S2 +S3)/2,ax.get_ylim()[0]+10, "Sector 3", horizontalalignment='center', verticalalignment='center', fontsize=16, bbox=dict(facecolor='green', alpha=0.5))

	ax.text(0, ax.get_ylim()[0]-30, 'Author: Jerome Dormoy (jeromedormoy2@gmail.com)', fontsize=14)
	ax.text(S3, ax.get_ylim()[0]-30, 'Data source: F1TV App', fontsize=9, horizontalalignment='center')

	# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

	#ax.annotate(Err, )

	fig.set_size_inches(18.5, 10.5)

	# plt.show()
	plt.savefig('Plot_Out/Quali/'+Plot_File_Name)

	print('\nPlot', Plot_File_Name, 'saved!\n')




	# fig2, ax2 = plt.subplots()

	# for dist in Cumul_Distance_Table1:

	# 	Time_Delta = np.interp(Cumul_Distance_Table1[dist], Cumul_Distance_Table1, Live_Timing_1) 

	# ax2.plot(Cumul_Distance_Table1, Time_Delta, marker = '', color='white', label=Err1, alpha = 1)
	# # ax2.plot(Cumul_Distance_Table2, Live_Timing_2, linestyle='--', color='r', label=Err2)
	# ax2.legend(loc='center', bbox_to_anchor=(-.05, 0, 0, 0), shadow=True, ncol=1, fontsize = 13)

	# plt.show()

	return
# Plot_Data('1','2')

while True:
	File1, File2 = Choose_File()
	try:
		Plot_Data(File1, File2)
	except:
		print('Invalid files.')
		pass
	yn = input('\nNew Plot? (y/n)')

	if yn !='y':
		break

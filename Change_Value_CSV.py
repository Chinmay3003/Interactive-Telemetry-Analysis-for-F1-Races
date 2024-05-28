import math
import pandas as pd
import numpy as np
import os
import re

import time
import pytesseract as tess

import cv2 

directory='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Output/Quali/'
ArchiveDir ='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/Archive'



def LoopThru():
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            test = False

            DF = pd.read_csv(directory+filename)

            print(DF.head())

            Name = input('Input name (empty if good): ')
            # Track = input('Input track (empty if good): ')
            Lap_Time = input('Input lap time (empty if good): ')
            Session = input('Input Session (empty if good): ')


            if Name != '':
                DF['Driver'] = Name
                test = True

            
            # if Track != '':


            if Lap_Time != '':
                DF['Lap Time'] = Lap_Time
                test = True

            if Session != '':
                test = True
                DF['Lap'] = Session
            if test == True:
                print(DF.head())
                DF.to_csv(directory+filename, index=False )

LoopThru()
def Infinite():
    while True:
        LoopThru()
        print('Looking for Video to Rename!')
        time.sleep(1)


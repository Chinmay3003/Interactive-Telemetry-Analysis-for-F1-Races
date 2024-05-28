import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import csv

import pytesseract as tess
import os
import cv2
import re

import numpy as np

import tkinter as tk
from tkinter import filedialog

import time 


root = tk.Tk()
root.withdraw()



path = filedialog.askopenfilename()
# path='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/AUT_RUS_Q2.mov'

img = cv2.VideoCapture(path)

Perc = 50



frame = 1

img.set(1, frame)

ret, currentFrame = img.read()
print('Original Dimensions : ',currentFrame.shape)

width = int(currentFrame.shape[1] * Perc / 100)
height = int(currentFrame.shape[0] * Perc / 100)
dim = (width, height)

resized = cv2.resize(currentFrame, dim, interpolation = cv2.INTER_AREA)
 
print('Resized Dimensions : ',resized.shape)
 
cv2.imshow("Resized image", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()


roi = currentFrame[16:43, 14:83]
roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
# (thresh, roi) = cv2.threshold(roi, 75, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('roi', roi)
cv2.waitKey(0)
cv2.destroyAllWindows()


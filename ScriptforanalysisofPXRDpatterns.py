# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 15:41:45 2022

@author: mbar1
"""

#%% Batch area tracer
# Instructions (This code was written in UI Syder and is reccommended to be run cell by cell)
# Run cell 1 select first pattern-> select first file, then select ENTIRE data series
# Run cell 2, tune the baseline fitting to hearts content
# Run cell 3, this imports all in-situ runs
# Run cell 4,  this calculates the area under the peak using the trapezoidal rule, it also groups the x-values to pairs finds the average as a way to label the peaks
# OPTIONAL Run cell 5, this cell plots area as a function of time for each tracked peak
# OPTIONAL run cell 6 to plot all spectra on one plot 
#Optional save all patterns to separate sheet in excel workbook
#Note XRD files must be .xyd if other file type is desired code will have to be tweaked.
#%% Cell 1: import and calculate baseline:
import tkinter
from tkinter import Button
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import Pack
from tkinter import Text
from tkinter import Radiobutton
from tkinter import IntVar
from tkinter import StringVar
from tkinter import filedialog
from statistics import mean
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from os import listdir
from os.path import isfile, join, split
from matplotlib.widgets import Cursor
import scipy
from scipy.stats import linregress
import peakutils 
from openpyxl import load_workbook

# Button Definitions
def choose_firstfile():
    global filename1
    filename1 = tkinter.filedialog.askopenfilename()
def choose_patterns():
    global filename2
    filename2 = tkinter.filedialog.askopenfilenames()
    win_openingwindow.destroy()
    
    
# Window Creation
win_openingwindow = tkinter.Tk()
win_openingwindow.title('Please select files')
#first button
button_firstpattern = tkinter.Button(win_openingwindow,text='1: Choose the first pattern',command=choose_firstfile)
#second button
button_patterns = tkinter.Button(win_openingwindow,text='2: Choose the entire insitu run',command=choose_patterns)

button_firstpattern.place(x=120, y=25)
button_patterns.place(x=110, y=75)

win_openingwindow.geometry("400x150+10+10")
#defining infinite loop to display window (until button for file selection is pressed)
win_openingwindow.mainloop()
#%% Cell 2: Baseline subtraction and peak selection
df = pd.read_csv(filename1,delim_whitespace=True, header=None)
df.columns = ['2 theta','Intensity']
baseline_subtracted = df.copy()
#Change baseline fitting parameters here also look at thresh and tol if needed (other fitting params)
base=peakutils.baseline(df['Intensity'],deg=12)
baseline_subtracted['Intensity']=(df['Intensity']-base)
# Shows baseline subtraction(may need tweaking) and allows users to select peak ranges of interest for area calculations
fig,ax = plt.subplots()
ax.plot(df['2 theta'],baseline_subtracted['Intensity'], label='Baseline Subtracted')
ax.plot(df['2 theta'],df['Intensity'], label='Raw Data')
ax.plot(df['2 theta'],base, label='Baseline')
ax.legend()
ax.set_xlabel(r"$2\theta$")
ax.set_ylabel('Intensity')
ax.set_title('Please check baseline and select:\n to the left and right of all interested peaks')
# Determination the slope and y intercept to convert x points to indices (used later to define area under the curve to be integrated)
a = [0,1,2,3,4,5]
twothetaparam = linregress(a, df['2 theta'][0:6])

# Defines cursor for storage of points
cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                color = 'r', linewidth = 1)
# Creating an annotating box
annot = ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points",
                    bbox=dict(boxstyle='round4', fc='linen',ec='k',lw=1),
                    arrowprops=dict(arrowstyle='-|>'))
annot.set_visible(False)
# Function for storing and showing the clicked values (repurposed from stack exchange)
coord = []
xvalues=[]
def onclick(event):
    global coord
    coord.append((event.xdata, event.ydata))
    x = event.xdata
    y = event.ydata
    xvalues.append(x)
    annot.xy = (x,y)
    text = "({:.2g}, {:.2g})".format(x,y)
    annot.set_text(text)
    annot.set_visible(True)
    fig.canvas.draw() #redraw the figure
    
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

#%% Cell 3: Importing and subtracting all in-situ patterns
# Importing from inputted file names
for fileNameindex in range(len(filename2)): 
    fileName=filename2[fileNameindex]
    if filename2[fileNameindex][-3:]=='xyd': 
        df2=pd.read_csv(fileName,delim_whitespace=True, header=None)
        df2.columns = ['2 theta','Intensity']
    # Background subtraction for all in-situ run files
        backgroundsubtract=df.copy()
        backgroundsubtract['Intensity']=((df2['Intensity'])-base)
        if fileNameindex==0:
            overalldf=backgroundsubtract.copy()
            overalldf[fileName + " Intensity"]=backgroundsubtract["Intensity"].copy()
            overalldf.drop(columns=["Intensity"], inplace=True)
        else:
            overalldf[fileName + " Intensity"]=backgroundsubtract["Intensity"].copy()

#%% Cell 4: Calculating the area under the peak:
areas = pd.DataFrame()
#Makes pairwise list of selected x values
pairx = list(zip(xvalues[::2], xvalues[1::2]))
#Labels peaks by 2theta:
overallarea = []
trackedpeaks = []
for i in range(len(pairx)):
    areas = []
    trackedpeaks.append(str(round(mean(pairx[i]),3)))
    for columnIndex in range(len(overalldf.columns[1:])):      
        columnName = overalldf.columns[1:][columnIndex] 
        areas.append(np.trapz(overalldf[columnName][round(((pairx[i][0]-twothetaparam[1])/twothetaparam[0])):round(((pairx[i][1]-1.98)/0.015))]))
    overallarea.append(tuple(areas))
temp = np.transpose(overallarea)
areadf = pd.DataFrame(temp,columns=trackedpeaks)
#Saves file as folder name where all data is stored, file is saved one folder up from where all files are saved
savename = filename1.split(r"/")
foldernam = r"/".join(savename[:-2])
filenam = (savename[-2])
areadf.to_excel(foldernam+"//"+ filenam +".xlsx")  
#%% OPTIONAL Cell 5: Plot to see area as function of time
fig,ax = plt.subplots()
for columnIndex in range(len(areadf.columns[0:])):      
    columnName = areadf.columns[0:][columnIndex] 
    ax.plot(areadf[columnName],zorder=columnIndex)
ax.legend(labels=trackedpeaks)
ax.set_xlabel(r"$2\theta$")
ax.set_ylabel('Integrated Intensity')

#%% OPTIONAL Cell 6: Plot to see all curves with baseline subtraction
fig,ax = plt.subplots()
for columnIndex in range(len(overalldf.columns[1:])):      
    columnName=overalldf.columns[1:][columnIndex] 
    ax.plot(overalldf[overalldf.columns[0]],overalldf[columnName],zorder=1+columnIndex)
ax.set_xlabel(r"$2\theta$")
ax.set_ylabel('Intensity')

#%% OPTIONAL Cell 7: To save all baseline subtracted patterns from the overall dataframe to sheet in excel workbook:
path=foldernam+"//"+ filenam +".xlsx"
book = load_workbook(path)
writer = pd.ExcelWriter(path, engine = 'openpyxl')
writer.book = book
overalldf.to_excel(writer, sheet_name = 'baseline subtracted')
writer.close()

    


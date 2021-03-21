'''
Monitor Grapher v0.1

Plots Sunlight Logger data from CSV file.

   Copyright 2020 Nezumi Workbench

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''   

import csv
from pprint import pprint
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

FS_THRESHOLD = 76

with open('GARDEN.CSV') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    dataSets = []
    dateTimes = []
    resistances = []
    timeStart = ''
    timeStop = ''
    fsMins = 0
    foundStartTime = False

    for row in readCSV:
        print(row)
        if 'Title: ' in row[0]:
            # Add the following Dict
            # {"title": string, dateTimes: list: "resistances": list  }
            # append Dict to datasets list
            # null out dateTimes and Resistances
            # Calc Start Time, End Time, Avg intensity.
            dataSet = {'title': row[0][7:], 'dateTimes': dateTimes, 'resistances': resistances}
            dataSets.append(dataSet)
            # I could just generate the plots here.
            fig, ax = plt.subplots()
            textstr = '\n'.join((
                f'start time: {timeStart}',
                f'stop time: {timeStop}',
                f'Hours Full Sun {fsHrs}'
            ))
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            # place a text box in middle top in axes coords
            ax.text(0.20, 0.95, textstr, transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=props)

            title = f"{dataSet['title']}\n{run_date}"

            ax.plot(np.array(dataSet['dateTimes']),np.array(dataSet['resistances']))
            ax.set(xlabel='time', ylabel='resistance (ohms)', title=title)
            xfmt = mdates.DateFormatter('%H:%M')
            ax.xaxis.set_major_formatter(xfmt)
            # ax.xaxis.set_major_formatter(hours_fmt)
            # ax.xaxis.set_minor_locator(months)
            plt.ylim(0, 500)
            plt.xlim(dataSet['dateTimes'][0].replace(hour=6), dataSet['dateTimes'][0].replace(hour=20))
            
            ax.grid()

            fig.savefig(dataSet['title'].replace(" ", "_") + ".png")
            plt.show()

            dateTimes = []
            resistances = []
            timeStart = 0
            timeStop = 0
            fsMins = 0
            foundStartTime = False
        else:
            dateTimes.append(datetime.strptime(row[0], '%Y/%m/%dT%H:%M:%S'))
            resistances.append(float(row[1]))
            run_date = datetime.strptime(row[0], '%Y/%m/%dT%H:%M:%S').strftime("%Y/%m/%d")
            if float(row[1]) < FS_THRESHOLD:
                if not foundStartTime:
                    timeStart = datetime.strptime(row[0], '%Y/%m/%dT%H:%M:%S').strftime("%H:%M")
                    foundStartTime = True
                timeStop = datetime.strptime(row[0], '%Y/%m/%dT%H:%M:%S').strftime("%H:%M")
                fsMins += 1
                fsHrs = "{:.1f}".format(fsMins/60)


pprint(dataSets)

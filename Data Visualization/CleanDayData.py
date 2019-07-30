'''
@author: Matthew Estopinal

Instructions: If you do not have traffic CSVs, first run TrafficDATToCSV.py on the
.dat data from TDOT. From there, pick each CSV you would like to reduce to a cleaner format,
and place them all in their own folder. Then, run this script from the editor or terminal.
This script is not required to be in the same folder as the data, it can be run from anywhere.
You will be prompted for input for the location of the data, and where it should be saved
Make sure that the folder input ends with a slash or it might not work correctly.
If the input and output folder match, the old data will be overwritten with
the new clean format.
'''
#TODO: Perhaps implement this script with TrafficDATToCSV in order to only
#create cleanly formatted data.


from DayOfData import DayOfData as day
import csv
import os

#Goes through the CSVs and writes new CSVs with a cleaner data format
#input is the names of files, in string format
#Does not return output
def generateClean(inputFile, outputFile):
    print(inputFile)
    myDay = day(inputFile)
    with open(outputFile, 'w', newline='') as w:
        writer = csv.writer(w, delimiter=',')
        writer.writerow(['Time(hr)', 'Speed(m/s)', 'Flow(veh/hour)', 'Density(veh/mile)'])
        for i in range(len(myDay.time)):
            line = []
            line.append(str(myDay.time[i]))
            line.append(str(myDay.speed[i]))
            line.append(str(myDay.flow[i]))
            line.append(str(myDay.density[i]))
            writer.writerow(line)
 
#Gets the directories to read and write data to, then runs generateClean  
#Input is two directories on the machine in string format
#Does not return output
def cleanFolder(inputFolder, outputFolder):
    for file in os.listdir(inputFolder):
        if file.endswith('.csv'):
            inFile = inputFolder + file
            outFile = outputFolder + file
            generateClean(inFile, outFile)

#I would reccomend placing the data that you want to clean into a folder by itself
#the program loops through every CSV file in the given folder.
if __name__ == "__main__":
    inputFolder = input('Folder to get data from: ')
    outputFolder = input('Folder to output data(will overwrite if same folder is given):')
    cleanFolder(inputFolder, outputFolder)
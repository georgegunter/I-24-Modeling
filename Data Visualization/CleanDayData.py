from DayOfData import DayOfData as day
import csv
import os

#Goes through the CSVs and writes new CSVs with a cleaner data format
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
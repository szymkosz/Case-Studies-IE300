import csv
import matplotlib.pyplot as plt

fileName = "FlightDelay.csv"

'''Read Flight Delay data into program'''
flightDelayData = []
with open(fileName, 'r') as file:
    myReader = csv.reader(file)
    next(myReader)
    for line in myReader:
        flightDelayData.append(line)

for i in flightDelayData:
    if (int(i[3]) + int(i[4]) > 15):
        i.append("Y")
    else:
        i.append("N")
    print(i)

import csv
import matplotlib.pyplot as plt

fileName = "FlightDelay.csv"

'''Read Flight Delay data into program'''
rawFlightDelayData = []
with open(fileName, 'r') as file:
    myReader = csv.reader(file)
    next(myReader)
    for line in myReader:
        rawFlightDelayData.append(line)

### Classify each flight as Delayed/Not Delayed (Y/N)
for i in rawFlightDelayData:
    if (int(i[3]) + int(i[4]) > 15):
        i.append("Y")
    else:
        i.append("N")

### Isolate each airline, origin, and destination into a list
airlines = []
origins = []
destinations = []

for element in rawFlightDelayData:
    if element[0] not in airlines:
        airlines.append(element[0])
    if element[1] not in origins:
        origins.append(element[1])
    if element[2] not in destinations:
        destinations.append(element[2])

### Separate each attribute per airline

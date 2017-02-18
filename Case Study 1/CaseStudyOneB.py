import csv
import matplotlib.pyplot as plt

fileName = "FlightDelay.csv"
m = 3           # m-value for M-estimates

'''Read Flight Delay data into program'''
rawFlightDelayData = []
with open(fileName, 'r') as file:
    myReader = csv.reader(file)
    next(myReader)
    for line in myReader:
        rawFlightDelayData.append(line)

''' Classify each flight as Delayed/Not Delayed (Y/N) '''
for i in rawFlightDelayData:
    if (int(i[3]) + int(i[4]) > 15):
        i.append("Y")
    else:
        i.append("N")

''' Isolate each airline, origin, and destination into a list '''
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

''' Separate each attribute per airline '''
airlineFlightDelay = {k: {} for k in airlines}
for key in airlineFlightDelay.keys():
    for origin in origins:
        airlineFlightDelay[key][origin] = {}
        airlineFlightDelay[key][origin]["Y"] = 0
        airlineFlightDelay[key][origin]["N"] = 0
    for dest in destinations:
        airlineFlightDelay[key][dest] = {}
        airlineFlightDelay[key][dest]["Y"] = 0
        airlineFlightDelay[key][dest]["N"] = 0

''' Increment Y/N attribute per airport per airline '''
numDelay = 0
numNoDelay = 0

for i in rawFlightDelayData:
    airlineFlightDelay[i[0]][i[1]][i[5]] += 1
    airlineFlightDelay[i[0]][i[2]][i[5]] += 1

  ## Count Total Delay/No Delay
    if i[5] == "Y":
        numDelay += 1
    elif i[5] == "N":
        numNoDelay += 1

### Pre-calculate probabilities
P_ORIGIN = 1/len(origins)
P_DESTINATION = 1/len(destinations)
P_CARRIER = 1/len(airlines)
numOfObsv = len(rawFlightDelayData)

probY = numDelay/numOfObsv
probN = numNoDelay/numOfObsv


# Neatly prints all data per airline
'''
for key in airlineFlightDelay.keys():
    print(key)
    for i in airlineFlightDelay[key]:
        print(i, airlineFlightDelay[key][i])
'''

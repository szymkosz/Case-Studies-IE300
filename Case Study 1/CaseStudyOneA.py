import csv
import matplotlib.pyplot as plt

fileName = "FlightTime.csv"
minFlightTime = 230
precision = 3           # Precision of output numbers

'''Target Flight Time Variables'''
d = 1741.16             # distance (mi) used in target flight time eq
lori = -87.90           # longitudinal coord. of origin
ldes = -118.41          # longitudinal coord. of destination


'''Read Flight Time data into program'''
flightData = []
with open(fileName, 'r') as file:
    myReader = csv.reader(file)
    next(myReader)
    for line in myReader:
        if int(line[9]) < minFlightTime:
            continue
        flightData.append(line)


'''Calculate number of observations and Target Flight Time'''
numOfObsv = len(flightData)
TFT = (0.117 * d) + (0.517 * (lori - ldes)) + 20
TFT = round(TFT, precision)


'''Calculate Typical Time'''
oriDelay = []           # delay data for origin airport
desDelay = []           # delay data for destination airport

### Isolate delay data and append into dedicated dicts
for element in flightData:
    oriDelay.append(int(element[6]))
    desDelay.append(int(element[8]))

### Calculate average ori/des delays
avgOriDelay = 0         # initialize average origin delay
avgDesDelay = 0         # initialize average destination delay

for element in desDelay:
    avgDesDelay += element
avgDesDelay /= len(desDelay)

for element in oriDelay:
    avgOriDelay += element
avgOriDelay /= len(oriDelay)

typicalTime = TFT + avgOriDelay + avgDesDelay
typicalTime = round(typicalTime, precision)

### Function takes in a list of numbers and returns the average
def listAverage(delayData):
    total = 0
    for element in delayData:
        total += int(element)
    average = total / len(delayData)
    return average


'''Time Added per Airline''' # Average Flight Time - Target Flight Time
airlines = []                   # list containing all airlines in data

### Isolate each airline into a list
for element in flightData:
    if element[1] not in airlines:
        airlines.append(element[1])

# Create a dictionary that maps airline name to a list of delay data
airlineFlightTimes = {k: [] for k in airlines}
for element in flightData:
    airlineFlightTimes[element[1]].append(element[9])

# Separate flight times per airline
avgAirlineFlightTime = []
timeAdded = []
timeAddedDict = {}

for airline in airlines:
    flightAvg = listAverage(airlineFlightTimes[airline])
    avgAirlineFlightTime.append((airline, flightAvg))
    timeAdded.append((airline, round((flightAvg - typicalTime), precision)))
    timeAddedDict[airline] = (flightAvg - typicalTime)


'''Output calculations into a text file'''
text_file = open("PartA_Output.txt", 'w')
text_file.write("IE 300 -- CASE STUDY 1, PART A -- Feb. 23, 2017\n\n\n")


# ---> text_file.write()
### Number of observations
text_file.write("Number of observations: " + str(numOfObsv) + '\n')

### Target flight time
text_file.write("Target Flight Time: " + str(TFT) + " min" + '\n\n')

### Typical time
text_file.write("Typical Time: " + str(typicalTime) + " min" + '\n\n')

### Time added for each airline
text_file.write("   Time added for \n\n")
for element in timeAdded:
    text_file.write("               " + str(element[0]) + ": " + str('{:>8}'.format(element[1])) + " min" + '\n')

##### Lowest time added?
lowestTime = float(timeAdded[0][1])
lowestAirline = ''
for stat in timeAdded:
    if stat[1] < lowestTime:
        lowestTime = stat[1]
        lowestAirline = stat[0]
    else:
        continue

text_file.write("\nAirline with lowest time added is " + str(lowestAirline) + " with " + str(lowestTime) + " min.")

text_file.close()

'''Plotting the data'''
# Plot data
plt.bar(range(len(timeAddedDict)), timeAddedDict.values() , align="center", color='c')
plt.xticks(range(len(timeAddedDict)), list(timeAddedDict.keys()))


# Plot Labels
plt.title("Time Added (ORD --> LAX)")
plt.xlabel("Airline")
plt.ylabel("Time Added (min)")

#plt.show()

'''Exporting Graph into PDF'''
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages('TimeAddedGraph.pdf') as pdf:
    pdf.savefig()

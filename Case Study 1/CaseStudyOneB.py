import csv

precision = 7           ## Precision of output probabilities

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
    delayTime = float(i[3]) + float(i[4])
    if delayTime > 15:
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

    # Count Total Delay/No Delay
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


'''Write a function that calculates required probability based on input'''
## Function takes three string parameters--Origin, Destination, and Airline
## Returns P(Delay | Ori, Dest, Carr) and P(No Delay | Ori, Dest, Carr)
def probability(ori, dest, carr):

    ## Initialize counter variables
    numOriY = 0; numOriN = 0
    numDestY = 0; numDestN = 0
    numCarrY = 0; numCarrN = 0

    ## Calculates number of Delay/NoDelay for Origin/Destination
    for i in airlines:
        numOriY += airlineFlightDelay[i][ori]["Y"]
        numOriN += airlineFlightDelay[i][ori]["N"]
        numDestY += airlineFlightDelay[i][dest]["Y"]
        numDestN += airlineFlightDelay[i][dest]["N"]

    ## Calculates number of Delay/NoDelay for Airline
    for i in airlineFlightDelay[carr]:
        numCarrY += airlineFlightDelay[carr][i]["Y"]
        numCarrN += airlineFlightDelay[carr][i]["N"]

    numCarrY /= 2       ## Must account for double counting
    numCarrN /= 2       ## (Once for Origin and once for Destination)

    ## Calculates probability of Delay/NoDelay for Origin/Dest/Airline
    pOriY = ((numOriY + m * P_ORIGIN)/(numDelay + m))
    pOriN = ((numOriN + m * P_ORIGIN)/(numNoDelay + m))
    pDestY = ((numDestY + m * P_DESTINATION)/(numDelay + m))
    pDestN = ((numDestN + m * P_DESTINATION)/(numNoDelay + m))
    pCarrY = ((numCarrY + m * P_CARRIER)/(numDelay + m))
    pCarrN = ((numCarrN + m * P_CARRIER)/(numNoDelay + m))

    ## Calculates P(Delay | Ori, Dest, Carr) and P(No Delay | Ori, Dest, Carr)
    pTotalY = (probY * pOriY * pDestY * pCarrY)
    pTotalN = (probN * pOriN * pDestN * pCarrN)

    delayed = (pTotalY > pTotalN)
    if delayed:
        delayed = "delayed"
    else:
        delayed = "not delayed"

    return '{:>10}'.format(round(pTotalY, precision)), '{:>10}'.format(round(pTotalN, precision)), delayed


'''Store Probability Calculations'''
### Number 1 -- JFK-LAS on AA
num1 = probability("JFK","LAS","AA")

### Number 2 -- JFK-LAS on B6
num2 = probability("JFK","LAS","B6")

### Number 3 -- SFO-ORD on VX
num3 = probability("SFO","ORD","VX")

### Number 4 -- SFO-ORD on WN
num4 = probability("SFO","ORD","WN")


'''Output calculations into a textfile'''
text_file = open("PartB_Output.txt", 'w')
text_file.write("IE 300 -- CASE STUDY 1, PART B -- Feb. 23, 2017\n\n\n")

### Number 1 -- JFK-LAS on AA
text_file.write("Number 1 -- JFK to LAS on American Airlines\n\n")
text_file.write("  P(Delay | JFK, LAS, AA):     " + str(num1[0]))
text_file.write("\n  P(No Delay | JFK, LAS, AA):  " + str(num1[1]))
text_file.write("\n  This flight is " + num1[2] + ".\n\n\n")

### Number 2 -- JFK-LAS on B6
text_file.write("Number 2 -- JFK to LAS on JetBlue\n\n")
text_file.write("  P(Delay | JFK, LAS, B6):     " + str(num2[0]))
text_file.write("\n  P(No Delay | JFK, LAS, B6):  " + str(num2[1]))
text_file.write("\n  This flight is " + num2[2] + ".\n\n\n")

### Number 3 -- SFO-ORD on VX
text_file.write("Number 3 -- SFO to ORD on Virgin Airlines\n\n")
text_file.write("  P(Delay | SFO, ORD, VX):     " + str(num3[0]))
text_file.write("\n  P(No Delay | SFO, ORD, VX):  " + str(num3[1]))
text_file.write("\n  This flight is " + num3[2] + ".\n\n\n")

### Number 4 -- SFO-ORD on WN
text_file.write("Number 4 -- SFO to ORD on Southwest Airlines\n\n")
text_file.write("  P(Delay | SFO, ORD, WN):     " + str(num4[0]))
text_file.write("\n  P(No Delay | SFO, ORD, WN):  " + str(num4[1]))
text_file.write("\n  This flight is " + num4[2] + ".\n\n\n")

text_file.close()

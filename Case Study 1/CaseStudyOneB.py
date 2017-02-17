import csv
import matplotlib.pyplot as plt

fileName = "FlightDelay.csv"

'''Read Flight Delay data into program'''
flightDelayData = []
with open(fileName, 'r') as file:
    myReader = csv.reader(file):
    next(myReader)
    for line in myReader:
        flightDelayData.append(line)

#!/usr/bin/env python3

import os
import math
import random

print("Script 1 Started!")

################################################
# File Management
################################################

# Current working directory
cwd = os.getcwd() + "/"

# For regular output (instead of printing
# to screen)
outputfilename = "script1.out"
outputfile = open(cwd+outputfilename,"w")

# For errors and exceptions
errorfilename = "script1.out"
errorfile = open(cwd+errorfilename,"w")

# Name of file holding data
file1filename = "file1.txt"

# Seed for random
SEED = 123
random.seed(SEED)

################################################
# Variables
################################################

# What time to start at (unix time in seconds
# starting from 00:00:00 Jan 1, 1970)
UNIXTIMESTART = 49 * 365 * 24 * 60 * 60
# Total time in seconds for this simulation
TOTALTIME = 5 * 365 * 24 * 60 * 60

# Fixed duration of time in seconds between
# each snapshot
SNAPSHOTDURATION = 10

# Mean Flyover time period in seconds
# (based off of the fact that there are
#  on average two flyovers per day)
FLYOVERTIME = 24 * 60 * 60 / 2
# Flyover time standard deviation
FLYOVERSPREAD = 60 * 5
# Flyover time "plus or minus" cutoff;
# express as a multiple of the spread
FLYOVERCUTOFF = 10

# Fixed Flyover Duration in seconds (since
# it seems like the satellite takes a few
# snapshots every flyover)
FLYOVERDURATION = 30

# Mean Eruption time in seconds
# (I'm just assuming there is one
#  eruption per year)
ERUPTIONTIME = 365 * 24 * 60 * 60
# Eruption time standard deviation
# (I'm just assuming it is two months)
ERUPTIONSPREAD = 2 * 30 * 24 * 60 * 60

# Longitude of Location (degrees?)
longitude = -155.30000
# Latitude of Location (degrees?)
latitude = 19.40000


################################################
# Useful Functions
################################################

# Computes the Year,Month,Day,Hour,Min from
# UNIX time

def getUCT(seconds):
    TotalSec = seconds
    TotalMin = TotalSec//60
    TotalHour = TotalMin//60
    TotalDay = TotalHour//24
    TotalMonth = TotalHour//30
    TotalYear = TotalDay//365

    Year = TotalYear + 1970
    Month = TotalMonth % 12
    Day = TotalDay % 30
    Hour = TotalHour % 24
    Min = TotalMin % 60

    return Year,Month,Day,Hour,Min

# Simple Box-Muller to give a flyover event
# over a normal distribution

def getFlyover():
    while True:
        rand1 = random.random()
        rand2 = random.random()
    
        dum1 = math.sqrt(-2*math.log(rand2))
        dum2 = 2*math.pi*rand1
    
        z1 = math.sin(dum2) * dum1
#       z2 = math.cos(dum2) * dum1
    
        if (abs(z1) < FLYOVERCUTOFF): break

    return int(z1 * FLYOVERSPREAD + \
               FLYOVERTIME)

# Simple Box-Muller to give an event
# (in this case, an eruption)
# over a normal distribution

def getEvent():
    while True:
        rand1 = random.random()
        rand2 = random.random()
    
        dum1 = math.sqrt(-2*math.log(rand2))
        dum2 = 2*math.pi*rand1
    
        z1 = math.sin(dum2) * dum1
#       z2 = math.cos(dum2) * dum1

        if (True): break

    return int(z1 * ERUPTIONSPREAD + \
               ERUPTIONTIME)

# Apply Planck's Blackboy Radiation
# Law to get the theoretical
# spectral radiance at some
# temperature and wavelength

def getSpectralRadiance(temperature,wavelength):

    return c1 / ((wavelength**5)* \
            (math.exp(c2 / (wavelength * \
                      temperature)) - 1.0))

# Evaluate NTI given the two wavelengths
# (4 micrometer and 12 micrometer)
# as specified in MODVOLC

def getNTI(wavelength4,wavelength12):

    return (wavelength4 - wavelength12) / \
           (wavelength4 + wavelength12)

# Get the average temperature, adjusted
# by time of day and season

def getAverageTemperature(month,day,hour,minute):

    temperature = 27.0

    return temperature

################################################
# The Main Loop
################################################
    
file1 = open(cwd+file1filename,"w")
file1.write("{:10s} {:3s} {:4s} {:2s} {:2s} {:2s} {:2s}\n".format(\
            "UNIX_Time","Sat","Year","Mo","Dy","Hr","Mn") )

t = UNIXTIMESTART
UNIXTIMEEND = UNIXTIMESTART + TOTALTIME

while True:

#   Figure out when the next event is
    print("t:", t)
    t = t + getEvent()

#   Always check if we are going over time
    if (t > UNIXTIMEEND): break

#   Start recording while this event occurs
#   The conditional checks when the event ends
    Tnext = 0
    eventOngoing = True
    while (eventOngoing):

#       Always check if we are going over time
        if (t+Tnext > UNIXTIMEEND): break

        print("Got here!")

#       Write to the file
        Year,Month,Day,Hour,Min = getUCT(t)
        print(t,"A",Year,Month,Day,Hour,Min)
        file1.write("{:10d}   {:1s} {:4d} {:02d} {:02d} {:02d} {:02d}\n".format(\
                t,"A",Year,Month,Day,Hour,Min) )

#       The next recording occurs when there is
#       another flyover
        Tnext = Tnext + getFlyover()
        eventOngoing = False

    t = t + Tnext

################################################

print("Script 1 Successfully Exited!")

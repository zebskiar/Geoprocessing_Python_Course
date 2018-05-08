# ############################################################################################################# #
# (c) Matthias Baumann, Humboldt-Universität zu Berlin, 4/23/2018
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
import time
import os
import gdal
# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #
rootdir = "D:/UNI/Python/Assignment02/data"

# ####################################### PROCESSING ########################################################## #

scneneDirs=[]
for scenes in os.listdir(rootdir):
    print(scenes)


# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
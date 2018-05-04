# ############################################################################################################# #
# (c) Matthias Baumann, Humboldt-Universität zu Berlin, 4/23/2018
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
import time
import os
import glob
import re
# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #
#SHP = "L:/_SHARED_DATA/CL_MB/tc_sc/_Version02_300m/points_300m_clip.shp"
#outputFile = "L:/_SHARED_DATA/CL_MB/tc_sc/_Version02_300m/points_300m_clip_summary.shp"
#buff_m = 100


# ####################################### PROCESSING ########################################################## #

### Exercise I - 1.
rootdir = "D:/UNI/Python/Assignment01/Assignment01_data/Part01_Landsat"

for names in os.listdir(rootdir):
    path_row = os.path.join(rootdir, names)
    print("For Path_Row", names)
    nLC08 = len(glob.glob1(path_row, "LC08*"))
    print("LC08 scenes:", nLC08)
    nLE07 = len(glob.glob1(path_row, "LE07*"))
    print("LE07 scenes:", nLE07)
    nLT05 = len(glob.glob1(path_row, "LT05*"))
    print("LT05 scenes:", nLT05)
    nLT04 = len(glob.glob1(path_row, "LT04*"))
    print("LT04 scenes:", nLT04)

### Exercise I - 2.a
LC08=[]
LE07=[]
LT05=[]
LT04=[]
for root, dirs, files in os.walk(rootdir):
    if "LC08" in root:
        LC08.append(root)
    if "LE07" in root:
        LE07.append(root)
    if "LT05" in root:
        LT05.append(root)
    if "LT04" in root:
        LT04.append(root)

corruptScenes=[]
for names in LC08:
    for root, dir, files in os.walk(names):
        if len(files)<19:
            corruptScenes.append(root)
for names in LE07:
    for root, dir, files in os.walk(names):
        if len(files)<19:
            corruptScenes.append(root)
for names in LT05:
    for root, dir, files in os.walk(names):
        if len(files)<21:
            corruptScenes.append(root)
for names in LT04:
    for root, dir, files in os.walk(names):
        if len(files)<21:
            corruptScenes.append(root)

print("# of Corrupted scenes:", len(corruptScenes))

### Exercise I - 2.a
file_path = os.path.join("D:/UNI/Python/Assignment01/","CorruptedScenes"+".txt")
file = open(file_path, "w")
for item in corruptScenes:
    file.write("%s\n" % item)
file.close()

### Exercise II - 1.
rootdir = "D:/UNI/Python/Assignment01/Assignment01_data/Part02_GIS-Files"

vec_count=0
ras_count=0
vec_list=[]
for files in os.listdir(rootdir):
    filename, ext = os.path.splitext(files)
    if ext in ".shp":
        vec_count += 1
        vec_list.append(filename)
    if ext in ".tif":
        ras_count += 1
print("# of SHP files:", vec_count)
print("# of TIF files:", ras_count)

### Exercise II - 2.
incompleteLayer=[]
for root, dirs, files in os.walk(rootdir):
    for name in vec_list:
        if (name+".dbf") not in files:
            incompleteLayer.append(name)
        if (name+".prj") not in files:
            incompleteLayer.append(name)

print("# of incomplete vector layers:", len(incompleteLayer))

file_path = os.path.join("D:/UNI/Python/Assignment01/","Corrupted_SHP"+".txt")
file = open(file_path, "w")
for item in incompleteLayer:
    file.write("%s\n" % item)
file.close()

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
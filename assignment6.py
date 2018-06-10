#
# Assignment VI – Calculation of local diversity indices
#
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import gdal
import numpy as np

# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/UNI/Python/Assignment06/data/"

# ####################################### PROCESSING ########################################################## #

def sdi(array_or_list):
    values, counts = np.unique(array_or_list, return_counts=True)
    if 0 in values:  # excluding classes set to 0 from sdi calculations
        counts = counts[1:len(counts)]
    sdi = -sum((float(n)/array_or_list.size) * np.log(float(n)/array_or_list.size) for n in counts if n is not 0)
    return sdi

sceneDirs = []
for file in os.listdir(wd):
    sceneDirs.append(wd+file)

for scene in sceneDirs:
    print("processing:", scene)
    ds = gdal.Open(scene)
    gt = ds.GetGeoTransform()
    rb = ds.GetRasterBand(1)
    pr = ds.GetProjection()
    dtype = rb.DataType
    ar = rb.ReadAsArray()
    ar[np.isin(ar, [4, 6, 7, 8, 9, 10, 12, 14, 15, 16, 20])] = 0  # set irrelevant classes to zero

    for buffer in [5, 10, 15]:
        print("sdi buffer:", buffer)
        out_ar = np.zeros(ar.shape, dtype=np.float)
        for x in range((0+buffer), (ar.shape[1]-buffer)):  # ar[0, buffer:-buffer]:
            for y in range((0+buffer), (ar.shape[0]-buffer)):  # ar[buffer:-buffer, 0]:
                win = ar[y-buffer:(y+buffer+1), x-buffer:(x+buffer+1)].copy()  # array window
                out_ar[y, x] = sdi(win)  # calc sdi for center cell of window

        # write raster
        file, ext = os.path.splitext(scene)
        outfile = file + "_sdi_" + str(buffer * 30) + "m_radius" + ext
        drvR = gdal.GetDriverByName('GTiff')
        outDS = drvR.Create(outfile, ar.shape[1], ar.shape[0], 1, gdal.GDT_Float32)
        outDS.SetProjection(pr)
        outDS.SetGeoTransform(gt)
        outDS.GetRasterBand(1).WriteArray(out_ar)
        outDS.FlushCache()
        del outDS


# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
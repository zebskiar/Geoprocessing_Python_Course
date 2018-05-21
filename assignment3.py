# ############################################################################################################# #
# (c) Matthias Baumann, Humboldt-Universität zu Berlin, 4/23/2018
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
import time
import os
import gdal
import arneTools as at
import numpy as np
import csv
# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #

rootdir = "D:/UNI/Python/Assignment03/data/"

# ####################################### PROCESSING ########################################################## #
ds = gdal.Open(rootdir+"DEM_Humboldt_sub.tif")
gt = ds.GetGeoTransform()
pr = ds.GetProjection()
rb = ds.GetRasterBand(1)
dtype = rb.DataType

sceneDirs = []
for scenes in os.listdir(rootdir):
    sceneDirs.append(rootdir+scenes)


### Exercise I

overlap = at.arneRT.overlapExtent(sceneDirs)
ncol = int((overlap[2]-overlap[0])/gt[1])
nrow = int((overlap[3]-overlap[1])/gt[5])

array = np.zeros((3, nrow, ncol), dtype=np.float)
for i in range(len(sceneDirs)):
    ds = gdal.Open(sceneDirs[i])
    gt = ds.GetGeoTransform()
    rb = ds.GetRasterBand(1)
    ar = rb.ReadAsArray()
    array[i, :, :] = rb.ReadAsArray(round((overlap[0]-gt[0])/gt[1]), round((overlap[1]-gt[3])/gt[5]), ncol, nrow)  # (origin_x, origin_y, sliceSize_x, sliceSize_y)

#print(array)
#print("Number of dimensions:", array.ndim)
#print("Shape of array:", array.shape)
#print("Size of the array:", array.size)
#print("Data type:", array.dtype)

dem = array[0, :, :]
slope = array[1, :, :]
thp = array[2, :, :]

dem_navalue = 65536.0
print("DEM mean:", round(np.mean(dem[dem < dem_navalue]), 2))
print("DEM min:", round(np.min(dem[dem < dem_navalue]), 2))
print("DEM max:", round(np.max(dem[dem < dem_navalue]), 2))

slope_navalue = -3.4028230607370965e+38
print("SLOPE mean:", round(np.mean(slope[slope > slope_navalue]), 2))
print("SLOPE min:", round(np.min(slope[slope > slope_navalue]), 2))  # no more values below 0
print("SLOPE max:", round(np.max(slope[slope > slope_navalue]), 2))

mask = (array[:2, :, :])
mask = np.where((mask[0, :, :] < 1000) & (mask[1, :, :] < 30), 1, 0)

outfile = rootdir + "DEM_sub1000_SLOPE_sub30.tif"
drvR = gdal.GetDriverByName('GTiff')
outDS = drvR.Create(outfile, ncol, nrow, 1, dtype)
outDS.SetProjection(pr)
gt_out = (overlap[0], gt[1], 0, overlap[1], 0, gt[5])
outDS.SetGeoTransform(gt_out)
outDS.GetRasterBand(1).WriteArray(mask, 0, 0)

print("Proportion of Area with elevation <1000 and slope <30:", str(round((mask[mask == 1].size / mask.size)*100, 2))+"%")


### Exercise II

with open(str(rootdir+"THP_mean_DEM_SLOPE.csv"), "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(["Year", "Mean_elev", "Mean_slope"])
    for year in range(1997, 2016):
        m_dem = round(np.mean(dem[(thp == year) & (dem < dem_navalue)]), 2)
        m_slope = round(np.mean(slope[(thp == year) & (slope > slope_navalue)]), 2)
        writer.writerow([year, m_dem, m_slope])


    # ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
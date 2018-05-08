# ############################################################################################################# #
# (c) Matthias Baumann, Humboldt-Universität zu Berlin, 4/23/2018
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
import time
import os
import gdal
import arneTools as at
# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #
rootdir = "D:/UNI/Python/Assignment02/data/"

# ####################################### PROCESSING ########################################################## #
def rasterExtend(rasterObject):
    gt = rasterObject.GetGeoTransform()
    ul_x = gt[0]
    ul_y = gt[3]
    lr_x = ul_x + (gt[1] * rasterObject.RasterXSize)
    lr_y = ul_y + (gt[5] * rasterObject.RasterYSize)
    extent = [ul_x, ul_y, lr_x, lr_y]
    return extent

def overlapExtent(rasterPathlist):
    ul_x_list = []
    ul_y_list = []
    lr_x_list = []
    lr_y_list = []
    overlap_extent = []
    for path in rasterPathlist:
        raster = gdal.Open(path)

        gt = raster.GetGeoTransform()
        ul_x = gt[0]
        ul_y = gt[3]
        lr_x = ul_x + (gt[1] * raster.RasterXSize)
        lr_y = ul_y + (gt[5] * raster.RasterYSize)

        ul_x_list.append(ul_x)
        ul_y_list.append(ul_y)
        lr_x_list.append(lr_x)
        lr_y_list.append(lr_y)

    overlap_extent.append(max(ul_x_list))
    overlap_extent.append(min(ul_y_list))
    overlap_extent.append(min(lr_x_list))
    overlap_extent.append(max(lr_y_list))

    return overlap_extent


sceneDirs=[]
for scenes in os.listdir(rootdir):
    sceneDirs.append(rootdir+scenes)

print("Individual raster extents (ul_x, ul_y, lr_x, lr_y):")
for path in sceneDirs:
    ras = gdal.Open(path)
    #gt = ras.GetGeoTransform()
    #print(gt)
    print(at.arneRT.rasterExtent(ras))

print("Extent of raster overlap (ul_x, ul_y, lr_x, lr_y):")
print(overlapExtent(sceneDirs))
print("UL (x,y):", overlapExtent(sceneDirs)[0], overlapExtent(sceneDirs)[1])
print("UR (x,y):", overlapExtent(sceneDirs)[2], overlapExtent(sceneDirs)[1])
print("LL (x,y):", overlapExtent(sceneDirs)[0], overlapExtent(sceneDirs)[3])
print("LR (x,y):", overlapExtent(sceneDirs)[2], overlapExtent(sceneDirs)[3])



# ####################################### END TIME-COUNT AND PRINT TIME STATS ################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
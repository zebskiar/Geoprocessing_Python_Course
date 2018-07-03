
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import gdal
import numpy as np
from joblib import Parallel, delayed

# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### CREATE JOB LIST ##################################### #

in_wd = "D:/UNI/Python/Assignment10/data/"
window_size = [5, 10, 15]
joblist = []
for file in os.listdir(in_wd):
    for size in window_size:
        joblist.append([str(in_wd+file), size])

# ####################################### MULTI-PROCESSING ########################################################## #

# define worker function
def SDI_moving_window(job):

    def sdi(array_or_list):
        values, counts = np.unique(array_or_list, return_counts=True)
        if 0 in values:  # excluding classes set to 0 from sdi calculations
            counts = counts[1:len(counts)]
        sdi = -sum(
            (float(n) / array_or_list.size) * np.log(float(n) / array_or_list.size) for n in counts if n is not 0)
        return sdi

    path = job[0]
    buffer = job[1]

    ds = gdal.Open(path)
    gt = ds.GetGeoTransform()
    rb = ds.GetRasterBand(1)
    pr = ds.GetProjection()
    ar = rb.ReadAsArray()
    ar[np.isin(ar, [4, 6, 7, 8, 9, 10, 12, 14, 15, 16, 20])] = 0  # set irrelevant classes to zero

    out_ar = np.zeros(ar.shape, dtype=np.float)
    for x in range((0 + buffer), (ar.shape[1] - buffer)):  # ar[0, buffer:-buffer]:
        for y in range((0 + buffer), (ar.shape[0] - buffer)):  # ar[buffer:-buffer, 0]:
            win = ar[y - buffer:(y + buffer + 1),
                  x - buffer:(x + buffer + 1)].copy()  # array window
            out_ar[y, x] = sdi(win)  # calc sdi for center cell of window

    # write raster
    path, ext = os.path.splitext(path)
    outfile = path + "_sdi_" + str(buffer * 30) + "m_radius" + ext
    outfile = outfile.replace("data", "out")
    drvR = gdal.GetDriverByName('GTiff')
    outDS = drvR.Create(outfile, ar.shape[1], ar.shape[0], 1, gdal.GDT_Float32)
    outDS.SetProjection(pr)
    outDS.SetGeoTransform(gt)
    outDS.GetRasterBand(1).WriteArray(out_ar)
    outDS.FlushCache()
    del outDS

# parallel processing
if __name__ == '__main__':
    Parallel(n_jobs=5)(delayed(SDI_moving_window)(i) for i in joblist)


# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
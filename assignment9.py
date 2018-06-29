
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
import time
import os
import gdal
import osr, ogr
import numpy as np
# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/UNI/Python/Assignment09/data/"

# ####################################### PROCESSING ########################################################## #

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

    overlap_extent.append(max(ul_x_list))  # x min
    overlap_extent.append(min(ul_y_list))  # y max
    overlap_extent.append(min(lr_x_list))  # x max
    overlap_extent.append(max(lr_y_list))  # y min

    return overlap_extent

def TransformGeometry(geometry, target_sref):
    '''Returns cloned geometry, which is transformed to target spatial reference'''
    geom_sref= geometry.GetSpatialReference()
    transform = osr.CoordinateTransformation(geom_sref, target_sref)
    geom_trans = geometry.Clone()
    geom_trans.Transform(transform)
    return geom_trans

scene_dirs = []
for file in os.listdir(wd):
    if file.endswith(".tif"):
        scene_dirs.append(wd+file)

# get spatial info of rasters (same srs and pixel size in this case)
gt = gdal.Open(scene_dirs[0]).GetGeoTransform()
srs = osr.SpatialReference()
srs.ImportFromWkt(gdal.Open(scene_dirs[1]).GetProjection())

overlap = overlapExtent(scene_dirs)  # extent of raster overlap
ncol = int((overlap[2]-overlap[0])/gt[1])  # no. columns of overlap arrays
nrow = int((overlap[3]-overlap[1])/gt[5])  # no. rows of overlap arrays

# convert rasters to arrays
array = np.zeros((len(scene_dirs), nrow, ncol), dtype=np.int16)  # create 3dimensional array for point value extraction
class_array = np.zeros((ncol*nrow, len(scene_dirs)), dtype=np.int16)  # create classification array (output)
for i in range(len(scene_dirs)):
    ds = gdal.Open(scene_dirs[i])
    gt = ds.GetGeoTransform()
    rb = ds.GetRasterBand(1)
    array[i, :, :] = rb.ReadAsArray(round((overlap[0]-gt[0])/gt[1]), round((overlap[1]-gt[3])/gt[5]), ncol, nrow)
    # above parameters: (origin_x, origin_y, sliceSize_x, sliceSize_y)
    class_array[:, i] = array[i, :, :].ravel()  # write entire raster into one column

# load points
driver = ogr.GetDriverByName('ESRI Shapefile')
SRC_points = driver.Open(wd+"RandomPoints.shp")
points = SRC_points.GetLayer()
pnt = points.GetNextFeature()

# create empty target arrays
train_array = np.zeros((0, len(scene_dirs)), dtype=np.int16)
label_array = np.zeros((0, 1), dtype=np.int16)

# loop through points
while pnt:
    print(pnt.GetField('Id'))
    pnt_label = pnt.GetField('Class')
    label_array = np.append(label_array, [[pnt_label]], axis=0)

    pnt_geom = pnt.GetGeometryRef()
    reprj_geom = TransformGeometry(pnt_geom, srs)  # transform point to raster srs
    pnt_x, pnt_y = reprj_geom.GetX(), reprj_geom.GetY()

    # check if point is within overlap
    if overlap[0] <= pnt_x <= overlap[2]:
        if overlap[1] >= pnt_y >= overlap[3]:

            # loop through 3rd raster array dimension
            pnt_values = [0, 0, 0, 0]
            for dim in range(np.shape(array)[0]):
                pnt_values[dim] = array[dim, int((pnt_y - overlap[1]) / gt[5]), int((pnt_x - overlap[0]) / gt[1])]  # convert coordinates to array index, read raster array value
            train_array = np.append(train_array, [pnt_values], axis=0)

    pnt = points.GetNextFeature()


# save resulting arrays to disc
np.save(wd+"trainingDS_features_"+str(np.shape(train_array)[1])+"_"+str(np.shape(train_array)[0])+".npy", train_array)
np.save(wd+"trainingDS_labels_"+str(np.shape(label_array)[1])+"_"+str(np.shape(label_array)[0])+".npy", label_array)
np.save(wd+"classificationDS_features_"+str(np.shape(class_array)[1])+"_"+str(np.shape(class_array)[0])+".npy", class_array)

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
# ############################################################################################################# #
#
# Assignment VII - Extract point information from various sources
#
# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
from osgeo import gdal, ogr, osr
import pandas as pd

# ####################################### SET TIME-COUNT ###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/UNI/Python/Assignment07/data/"

# ####################################### PROCESSING ########################################################## #

dem = gdal.Open(wd+"Elevation.tif")
dem_gt = dem.GetGeoTransform()
dem_ar = dem.GetRasterBand(1).ReadAsArray()

d2r = gdal.Open(wd+"DistToRoad.tif")
d2r_gt = d2r.GetGeoTransform()
d2r_ar = d2r.GetRasterBand(1).ReadAsArray()
d2r_ref = osr.SpatialReference()
d2r_ref.ImportFromWkt(d2r.GetProjection())

driver = ogr.GetDriverByName('ESRI Shapefile')
SRC_points = driver.Open(wd+"Points.shp")
points = SRC_points.GetLayer()
pnt = points.GetNextFeature()

SRC_old = driver.Open(wd+"Old_Growth.shp", 0)
old = SRC_old.GetLayer()
old_feat = old.GetNextFeature()
old_geom = old_feat.GetGeometryRef()
old_ref = old.GetSpatialRef()

SRC_priv = driver.Open(wd+"PrivateLands.shp", 0)
priv = SRC_priv.GetLayer()
priv_feat = priv.GetNextFeature()
priv_geom = priv_feat.GetGeometryRef()
priv_ref = priv.GetSpatialRef()


def reproj_point(point_geom, target_prj):
    source_prj = point_geom.GetSpatialReference()
    trans = osr.CoordinateTransformation(source_prj, target_prj)
    trans_geom = point_geom.Clone()
    trans_geom.Transform(trans)
    return trans_geom


out_df = pd.DataFrame(columns=["Point ID", "Variable", "Value"])
while pnt:
    pnt_id = pnt.GetField('Id')
    pnt_geom = pnt.GetGeometryRef()

    priv_pnt = reproj_point(pnt_geom, priv_ref)
    priv.SetSpatialFilter(priv_pnt)
    out_df.loc[len(out_df) + 1] = [pnt_id, "Private", priv.GetFeatureCount()]
    priv.SetSpatialFilter(None)

    old_pnt = reproj_point(pnt_geom, old_ref)
    old.SetSpatialFilter(old_pnt)
    out_df.loc[len(out_df) + 1] = [pnt_id, "OldGrowth", old.GetFeatureCount()]
    old.SetSpatialFilter(None)

    pnt_x, pnt_y = pnt_geom.GetX(), pnt_geom.GetY()
    pnt_elev = dem_ar[int((pnt_y - dem_gt[3]) / dem_gt[5]), int((pnt_x - dem_gt[0]) / dem_gt[1])]
    out_df.loc[len(out_df) + 1] = [pnt_id, "Elevation", pnt_elev]

    d2r_pnt = reproj_point(pnt_geom, d2r_ref)
    pnt_x, pnt_y = d2r_pnt.GetX(), d2r_pnt.GetY()
    pnt_d2r = d2r_ar[int((pnt_y - d2r_gt[3]) / d2r_gt[5]), int((pnt_x - d2r_gt[0]) / d2r_gt[1])]
    out_df.loc[len(out_df) + 1] = [pnt_id, "Road_Dist", pnt_d2r]

    print("finished with point", pnt_id)
    pnt = points.GetNextFeature()

out_df.to_csv(wd+"extracted_values.csv", index=None, sep=',', mode='a')

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
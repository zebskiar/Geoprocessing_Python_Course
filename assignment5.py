#Group I: Random Sampling
    #1) Get one PA
    #2) transform to EPSG 3035
    #3) Get extent of PA
    #4) Random Point within extent based on starting point (multitude of 30m)
    #5) Check if point within borders of PA (not extent)
    #6) Check if point has min x meters distance to nearest border
    #7) Check if x-coord. >= 90m
    #       else check if |y-coord| >= 90m
    #   --> both false, start again
    #   --> one TRUE save list1
    # while loop stopping at 50 entries

#Group II: Building the pixels
    # 9 Boxes by adding ad subtracting from given center points
    # add ID field for each 9 pixels and for each 9-pixel-box

#Group III: Coordinate system and shapefiles
    # EPSG 3035 because it is in meters


# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import ogr
from shapely import geometry
import random
import geopandas as gpd

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

wd       = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 7 - Vector processing II/Assignment05 - data/'
ger_path = 'gadm36_GERonly.shp'
pas_path = 'WDPA_May2018_polygons_GER_select10large.shp'
sp_path  = 'OnePoint.shp'

# ####################################### PROCESSING ########################################################## #

germany         = ogr.Open(wd + ger_path)
protected       = ogr.Open(wd + pas_path)
starting_point  = ogr.Open(wd + sp_path)

ger = germany.GetLayer()
pas = protected.GetLayer()
sp  = starting_point.GetLayer()

x_ori = sp.GetExtend()[0]
y_ori = sp.GetExtend()[2]

# FUNCTION to create random points
'''
def generate_random(number, polygon):
    list_of_points = []
    minx, miny, maxx, maxy = polygon
    counter = 0
    while counter < number:
        pnt = ogr.Geometry(ogr.wkbPoint)
        pnt.SetPoint_2D(0, random.uniform(minx, maxx), random.uniform(miny, maxy))
        if geom.Contains(pnt):
            pnt_list.append(pnt)
            counter += 1
    return list_of_points
'''

# loop through PAs
for pa in pas:
    #1) get pa
    print(pa.GetField('NAME')) #works

    #2) transform to EPSG 3035
    tmp = gpd.GeoDataFrame.from_file(wd + pas_path)
    PA_Lambert = tmp.to_crs(epsg=3035)
    #PA_Lambert.crs #not necessary
    PA_Lambert.to_file(wd + 'PA_Lambert.shp')
    PA_Lambert = ogr.Open(wd + 'PA_Lambert.shp')
    paslam = PA_Lambert.GetLayer() #we need to keep using this, but how do we do this if 'pa' is the loop-element?

    #3) get extent of pa
    geom = pa.GetGeometryRef()#works
    pa_ext = geom.GetEnvelope()#works

    #4) create random points a multitude of 30m away from starting point
    x_min, y_min, x_max, y_max = pa_ext
    pnt_list = []
    while len(pnt_list) < 3: #50, 3 as a test

        # find range of x coords to draw random number
        seq_x_min = x_ori + (int((x_min - x_ori) / 30)) * 30
        seq_x_max = x_ori + (int((x_max - x_ori) / 30)) * 30
        x_random = random.choice(range(seq_x_min, seq_x_max, 30))  # generate random x coordinate

        # find range of y coords to draw random number
        seq_y_min = y_ori + (int((y_min - y_ori) / 30)) * 30
        seq_y_max = y_ori + (int((y_max - y_ori) / 30)) * 30
        y_random = random.choice(range(seq_y_min, seq_y_max, 30))  # generate random y coordinate

        pnt = ogr.Geometry(ogr.wkbPoint)  # create point class object
        pnt.AddPoint(x_random, y_random)  # add point coordinate

        # 5) check if point within borders of PA (not extent) #works
        if geom.Contains(pnt):
            pnt_list.append(pnt)
    print(len(pnt_list)) #check if the while loop worked
    #print(pnt_list[0]) #check first point per PA
    x, y = pnt_list[0].GetX(), pnt_list[0].GetY() #how to get coordinates from point


    # The following needs to be included into the function above (generate_random):
    #6) check if point has min x meters distance to nearest border
        #find min distance to nearest border --> min_dist
        #min_dist < 60 (@Arne: Was it 60m?)

    # 7) Check if x-coord. >= 90m
    #       else check if |y-coord| >= 90m
    #   --> both false, start again
    #   --> one TRUE save list1
    # while loop stopping at 50 entries

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
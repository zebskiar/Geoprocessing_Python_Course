#######################################################
### Load shapefiles

import os
from osgeo import ogr, osr, gdal
import pandas as pd
import numpy as np
import shapefile


#shapefile to dataframe countries

#shp_path_CO = r"O:\Student_Data\DieckmannM\python2\groupwork\gadm36_dissolve.shp"
#shp_path_CO = r"D:\UNI\Python\Assignment04\data\gadm36_dissolve.shp"
shp_path_CO = r"D:\UNI\Python\Assignment04\data\GER_SUI_subset.shp"

sf_CO = shapefile.Reader(shp_path_CO)
#print(sf_CO)
#grab the shapefile's field names (omit the first psuedo field)
fields_CO = [x[0] for x in sf_CO.fields][1:]
records_CO = sf_CO.records()
shps_CO = [s.points for s in sf_CO.shapes()]
print(shps)
#write the records into a dataframe
CO_dataframe = pd.DataFrame(columns=fields_CO, data=records_CO)
#add the coordinate data to a column called "coords"
CO_dataframe = CO_dataframe.assign(coords=shps_CO)
print(CO_dataframe)
CO_dataframe.to_csv("D:\UNI\Python\Assignment04\data\pandas_CO.csv", sep=' ')


#shapefile to dataframe protected areas

shp_path_PA = r"D:\UNI\Python\Assignment04\data\subset_WDPA.shp"
sf_PA = shapefile.Reader(shp_path_PA)
print(sf_PA)
#grab the shapefile's field names (omit the first psuedo field)
fields_PA = [x[0] for x in sf_PA.fields][1:]
records_PA = sf_PA.records()
shps_PA = [s.points for s in sf_PA.shapes()]
#print(shps)
#write the records into a dataframe
PA_dataframe = pd.DataFrame(columns=fields_PA, data=records_PA)
#add the coordinate data to a column called "coords"
PA_dataframe = PA_dataframe.assign(coords=shps_PA)
print(PA_dataframe)
PA_dataframe.to_csv("O:\Student_Data\DieckmannM\python2\groupwork\pandas_PA.csv", sep=' ')


# needed variables:
# country
# MARINE (string) [0 (terrestrial),1 (coastal),2 (marine)]
# IUCN_CAT (string) [I-IV, not reported, not applicable]
# NAME (string)
# STATUS_YR (string)
# GIS_AREA (double)
# STATUS (string) [only designated & established]

# MARINE == 0
# STATUS == established OR designated


############################################################
### Processing Loop

##create empty dataframe
columns = ["country id", "country name", "pa_category", "# pa ", "pa_area", "largest_pa_area", "largest_pa_name", "largest_pa_year"]
output_dataframe = pd.DataFrame(columns=columns)

# loop over countries --> die Lösung die per mail diskutiert wurde benutzt einen while loop, evtl muss man das anpassen hier.
for co in #CO_SHP: #
    country_name = #### these depend on how the main loop is constructed,
    country_id = #### solutions for the while loop are already in the code discussed by mail

    # this is where we need to extract the attribute table of the PAs filtered by country (spatial):
    "EXTRACT PA-Attributes by country location ### For this we need the spatial information " \ # .GetField() call?
    "input shoul be the PA dataset thats already cleaned of marine and coastal PAs " \
    "*OR* the selection of PAs from which to select by country is set to terrestial only (if thats possible)" \
    "Output should be a panda table ("co_temp") containing the following attributes: IUCN_CAT, NAME, GIS_AREA, STATUS_YR"

    # country level statistics
    co_max_area = max(co_temp["GIS_AREA"])
    co_mean_area = np.mean(co_temp["GIS_AREA"])
    co_max_area_name = co_temp.loc[co_temp["GIS_AREA"] == co_max_area, "NAME"]
    co_max_area_year = co_temp.loc[co_temp["GIS_AREA"] == co_max_area, "STATUS_YR"]
    co_pa_count = co_temp.shape[0]

    output_co_level = [country_id, country_name, "ALL", co_pa_count, co_mean_area, co_max_area, co_max_area_name,
                        co_max_area_year]
    output_dataframe = output_dataframe.append(pd.DataFrame(data=output_co_level), ignore_index=True)

    # category level statistics
    # loop through subsets of PAs by category:
    for cat in pd.unique(co_temp["IUCN_CAT"]):
        cat_temp = co_temp.loc[co_temp["IUCN_CAT"] == cat]
        cat_max_area = max(cat_temp["GIS_AREA"])
        cat_mean_area = np.mean(cat_temp["GIS_AREA"])
        cat_max_area_name = cat_temp.loc[cat_temp["GIS_AREA"] == cat_max_area, "NAME"]
        cat_max_area_year = cat_temp.loc[cat_temp["GIS_AREA"] == cat_max_area, "STATUS_YR"]
        cat_pa_count = cat_temp.shape[0]

        output_cat_level = [country_id, country_name, str(cat), cat_pa_count, cat_mean_area, cat_max_area, cat_max_area_name,
                            cat_max_area_year]
        output_dataframe = output_dataframe.append(pd.DataFrame(data=output_cat_level), ignore_index=True)



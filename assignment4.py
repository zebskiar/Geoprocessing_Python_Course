#######################################################
### Load shapefiles

import os
from osgeo import ogr, osr, gdal
import pandas as pd
import numpy as np
import shapefile


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



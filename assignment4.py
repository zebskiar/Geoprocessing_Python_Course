#######################################################
### Load shapefiles

import os
from osgeo import ogr, osr, gdal
import pandas as pd
import shapefile


"........................"


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

output_dataframe = #panda frame with column names preallocated

# loop over countries
for co in #CO_SHP: #
    country_name = str(co)
    country_id = #id from panda table

    "EXTRACT PA-Attributes by country location ### For this we need the spatial information " \
    "input shoul be the PA dataset thats already cleaned of marine and coastal PAs " \
    "*OR* the selection of PAs from which to select by country is set to terrestial only (if thats possible)" \
    "Output should be a panda table ("co_temp") containing the following columns: pa_category, pa_name, pa_area, pa_year"

    # country level statistics
    co_max_area = max(co_temp["column area"])
    co_mean_area = max(co_temp["column area"])
    co_max_area_name =  # extract name from row with max area
    co_max_area_year =  # extract year from row with max area
    co_pa_count = len(co_temp)

    output_co_level = [country_id, country_name, "ALL", co_pa_count, co_mean_area, co_max_area, co_max_area_name,
                        co_max_area_year]
    output_dataframe = output_dataframe.append(pd.DataFrame(data=output_co_level), ignore_index=True)

    # category level statistics
    # loop through subsets of PAs by category:
    for cat in unique(pa_category)
        cat_temp = select from attributes where pa_category == cat
        cat_max_area = max(cat_temp["column area"])
        cat_mean_area = max(cat_temp["column area"])
        cat_max_area_name = #extract name from row with max area
        cat_max_area_year = #extract year from row with max area
        cat_pa_count = len(cat_temp)

        output_cat_level = [country_id, country_name, str(cat), cat_pa_count, cat_mean_area, cat_max_area, cat_max_area_name,
                            cat_max_area_year]
        output_dataframe = output_dataframe.append(pd.DataFrame(data=output_cat_level), ignore_index=True)





























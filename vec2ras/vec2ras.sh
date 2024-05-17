#!/bin/bash

vecpath="$1"
savepath="$2"
extent1=$3
extent2=$4
extent3=$5
extent4=$6
# layername="$crop"

# echo "-l vector -a DATASOURCE -ts 6663.0 8192.0 -a_nodata 0.0 -te $extent1 $extent2 $extent3 $extent4 -ot Float32 -of GTiff $vecpath $savepath"

gdal_rasterize -l output -a DATASOURCE -ts 6663.0 8192.0 -a_nodata 0.0 -te $extent1 $extent2 $extent3 $extent4 -ot Float32 -of GTiff $vecpath $savepath


# gdal_rasterize -l output -a DATASOURCE -ts 6663.0 8192.0 -a_nodata 0.0 -te 32.27233407 35.042919088 32.289032162 35.061888654 -ot Float32 -of GTiff /home/superworld/Documents/CPP/Superworld/SW/Projects/202304LandscapeSimilarity/GIS/ROAD/cy-road-final-crps/IMG0001_LT35.064_LG32.263000000000005/output.shp /home/superworld/Documents/CPP/Superworld/SW/Projects/202304LandscapeSimilarity/py-code/test.tif
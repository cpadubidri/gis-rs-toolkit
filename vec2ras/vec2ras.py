import os
from osgeo import ogr
import time

path="/media/superworld/Elements/CPPAdubidri/LANDSIMILARITY/CROPPED-ROAD"
save_path="/media/superworld/Elements/CPPAdubidri/LANDSIMILARITY/ROAD-MASK-3"

end=start=0
vector_list = os.listdir(path)
length = len(vector_list[3000:])
for vector in vector_list[3000:]:
	ex_time = end-start
	print("Converting {}, remaining {}, Expected fininish time {:.2f}".format(vector, length, ex_time*length/60))
	start = time.time()
	vecpath = os.path.join(path,vector,"output.shp")
	savepath = os.path.join(save_path,vector+'.tif')

	shapefile = ogr.Open(vecpath)

	layer = shapefile.GetLayer()

	# Get the extent of the layer
	extent = layer.GetExtent()
	extent1 = extent[0]
	extent2 = extent[2]
	extent3 = extent[1]
	extent4 = extent[3]
	# print(vecpath)

	os.system("./vec2ras.sh {} {} {} {} {} {}".format(vecpath, savepath, extent1, extent2, extent3, extent4, extent))
	length-=1
	end = time.time()

# gdal_rasterize -l vector -a DATASOURCE -ts 6663.0 8192.0 -a_nodata 0.0 -te 32.27233407 35.042919088 32.289032162 35.061888654 -ot Float32 -of GTiff $vecpath $savepath
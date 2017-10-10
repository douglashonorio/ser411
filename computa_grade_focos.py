# coding=utf-8
# coding=utf-8
# coding=utf-8
# coding=utf-8
# coding=utf-8
#enconding: uft-8
import sys
import os
import numpy as np

try:
    from osgeo import gdal, ogr, osr
except:
    sys.exit("Erro: a biblioteca GDAL não foi encontrada!")

from utils import *

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()

vector_file = "/programacao/focos/focos/focos-2015.shp"
vector_file_base_name = os.path.basename(vector_file)
layer_name = os.path.splittext(vector_files_base_name)[0]

spatial_extent = { 'xmin': -89.975, 'ymin': -59.975,
                   'xmax': -29.975, 'ymax': 10.025 }
spatial_resolution = { 'x': 0.05, 'y': 0.05}
grid_dimensions = { 'cols': 1200, 'rows': 1400}

file_format = "GTiff"
output_file_name = "/programacao/focos/focos/grade-2015.tif"
shp_focos = ogr.Open(vector_file)

if shp_focos is None:
    sys.exit("Erro: não foi possível abrir o arquivo '{0}'.".format(vector_file))

layer_focos = shp_focos.GetLayer(layer_name)
    if layer_focos is None:
        sys.exit("Erro: não foi possível abrir o arquivo '{0}' no arquivo (1}".format(layer()))
# encoding: utf-8

#Douglas Damião de Carvalho Honório 135518

#Importanto bibliotecas

import sys
import os
from numpy as np

try:
    from osgeo import gdal, ogr, osr
except:
    sys.exit("Erro: a biblioteca GDAL não foi encontrada!")

from utils import *

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()

vector_file = "C:/Programacao/Queimadas/focos/focos_2016.shp"

#Focos 2016
vector_file_base_name = os.path.basename(vector_file)

#Visualiza focus_2016
layer_name = os.path.splitext(vector_file_base_name)[0]

#cria uma matriz de dados (imagem)
spatial_extent = {'xmin': -89.975, 'ymin': -59.975, 'xmax': -29.975, 'ymax': 10.025}
spatial_resolution = {'x': 0.05, 'y': 0.05}
grid_dimensions = {'cols': 1200, 'rows': 1400}

file_format = "GTiff"



shp_focos = ogr.Open(vector_file)
if shp_focos is None:
    sys.exit("Erro: não foi possível abrir o arquivos '{0}'".format(vector_file))

layer_focos2 = shp_focos.GetLayer(layer_name)
if layer_focos2 is None:
    sys.exit("Erro: não foi possível acessar a camada '{0}' no arquivo '{1}'!".format(layer_name, vector_file))

sensores = {'TERRA_M-M', 'TERRA_M-T', 'AQUA_M-T', 'AQUA_M-M'}

#definindo os meses
for sensor in sensores:
    for mes in range(1, 13):
        layer_focos = layer_focos2

        if mes < 9:
            query = "satelite = '%s' and timestamp > '2016/0%s' and timestamp < '2016/0%s'" % (sensor, mes, mes + 1)

        elif mes ==9:
            query = "satelite = '%s' and timestamp > '2016/0%s' and timestamp < '2016/%s'" % (sensor, mes, mes + 1)

        else:
            query = "satelite = '%s' and timestamp > '2016/%s' and timestamp < '2016/%s'" % (sensor, mes, mes + 1)

        layer_focos.SetAttributeFilter(query)
        nfocos = layer_focos.GetFeatureCount()


# Saída de arquivos
output_file_path = "C:/Programacao/Queimadas/focos/"

        # Criando uma matriz numérica
        matriz = zeros((grid_dimensions['rows'], grid_dimensions['cols']), int16)

        #Calculando numero de focos
        for foco in layer_focos:
            location = foco.GetGeometryRef()
            col, row = Geo2Grid(location, grid_dimensions, spatial_resolution, spatial_extent)
            matriz[row, col] += 1

        # criando o tipo raster de saída
        driver = gdal.GetDriverByName(file_format)

        if driver is None:
            sys.exit("Erro: driver inexistente '{0}.".format(file_format))
        output_file_name = output_file_path + "Focos-" + sensor + "-" + str(mes) + ".tiff"
        raster = driver.Create(output_file_name, grid_dimensions['cols'], grid_dimensions['rows'], 1, gdal.GDT_UInt16)

        if raster is None:
            sys.exit("Erro: não foi possível criar o arquivo '{0}'.".format(output_file_name))

        raster.SetGeoTransform((spatial_extent['xmin'],spatial_resolution['x'],0,spatial_extent['ymax'],0,-spatial_resolution['y']))
        srs_focos = layer_focos.GetSpatialRef()
        raster.SetProjection(srs_focos.ExportToWkt())
        band = raster.GetRasterBand(1)
        band.WriteArray(matriz,0,0)
        band.FlushCache()
        raster = None
        
del raster, band

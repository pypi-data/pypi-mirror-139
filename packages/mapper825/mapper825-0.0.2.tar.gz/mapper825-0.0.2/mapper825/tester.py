
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import geopandas as gpd
from __init__ import mapper
import winsound

pd.set_option('display.max_columns', 500)

gdf = gpd.read_file(r'C:\Lucas\Laburo\0-Varios\data\data_in\base_icpag_full_etapas_qgis\base_icpag_full_etapas_qgis\base_icpag_full_etapas_qgis.shp')

mapper(
    gdf,
    'etap_24_0',
    r'C:\Lucas\Laburo\0-Varios\data\data_out\maps_out',
    footnote='Datos basados en la EPH de San justo primo'
)

winsound.MessageBeep()

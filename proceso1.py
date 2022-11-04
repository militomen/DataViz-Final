import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def carga_inicial():
  return pd.read_excel("ODC2022.xls")

# Se lee la información de forma óptima
odc = carga_inicial()

# Obtener parte de la información
odc_renombrado = odc.rename(columns={'TOTAL  FORESTAL':'AREA FORESTAL AFECTADA',
                                   'TOTAL OTRAS SUPERFICIES':'OTRAS AREAS AFECTADAS',
                                   'TOTAL SUPERFICIE AFECTADA':'AREA TOTAL AFECTADA'})

#odc_renombrado.dropna(subset=["Comuna"], inplace=True)
#geo_data = odc_renombrado
print(odc_renombrado)
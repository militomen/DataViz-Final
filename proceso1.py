import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.cluster import KMeans


#- Usar un archivo Excel como fuente de datos iniciales, con al menos 1000 registros. Puede ser un archivo propio o bien obtenido de alguna fuente pública, de cualquier forma, debe quedar disponible en el repositorio de entrega.
def carga_inicial():
  return pd.read_excel("ODC2022.xlsx")

odc = carga_inicial()

# Modificar algunos nombres de columnas de datos, independiente a que sean correctos, lo que se espera es la capacidad de cambiar sus nombres.
odc_renombrado = odc.rename(columns={'TOTAL  FORESTAL':'AREA FORESTAL AFECTADA',
                                   'TOTAL OTRAS SUPERFICIES':'OTRAS AREAS AFECTADAS',
                                   'TOTAL SUPERFICIE AFECTADA':'AREA TOTAL AFECTADA'})

#- Crear una columna de datos en el DataFrame, con la siguiente definición: “Fecha de Proceso”, 
# donde se debe registrar la fecha en que se está procesando el Excel. Tip: La misma fecha para
#  todos los registros en esa columna.
fecha_actual = datetime.datetime.now()
odc_renombrado['Fecha de Proceso'] = fecha_actual.strftime("%d-%m-%Y")

#- Crear una columna vacía en el DataFrame con el nombre “Clima”, después asignarle 
# valor de clima obtenido desde API de OpenWeatherMap, para esto aplicar una lógica 
# a elección propia, donde se evalúen al menos 2 columnas y el dato debe provenir de
#  al menos 5 comunas. Tip: se debe hacer la consulta de las 5 comunas antes de aplicar
#  el dato a la columna de Clima, similar al ejemplo de horarios en la clase final.
odc_renombrado['Clima'] = ("")
#Obtener lista de comunas resumidas
comunas = odc_renombrado["COMUNA"].sort_values().unique()

#Agrupar y sumar por la columna NUMERO DE INCENDIOS
agrupado = odc_renombrado.groupby(['COMUNA']).agg(
                                  {'NUMERO INCENDIOS ': 'sum' 
                                   #'Clima':'sum' 
                                   #'ultima_visita':'max'
                                  }).reset_index()
agrupado = agrupado.groupby(by='TOTAL SUPERFICIE AFECTADA').sum('NUMERO INCENDIOS ').sort_values(by='NUMERO INCENDIOS ', ascending=False)

kmeans = KMeans(n_clusters=4).fit(agrupado)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(odc_renombrado['NUMERO INCENDIOS '], odc_renombrado['TOTAL SUPERFICIE AFECTADA'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()

#Aplicar a la columna clima Segun el clima de la comuna y la cantidad de incendios
#Riesgo Alto, Medio, Bajo


#- El DataFrame resultante, debe ser almacenado en una base de datos local


#- Obtener los registros de la base de datos y exportar a un nuevo archivo Excel y otro archivo CSV.



import streamlit as st

import pydeck as pdk
import numpy as np
import pandas as pd


# Se importan funcionalidades desde librería propia
from utils import data_incendio
"""
def data_incendio():
  # Se lee Excel de datos
  incendios=pd.read_excel("ODC2022.xlsx")

  # Obtener columnas de datos
  #data_comuna = incendios[ ["REGION","PROVINCIA", "COMUNA", "NUMERO INCENDIOS ", "TOTAL  FORESTAL ", "TOTAL OTRAS SUPERFICIES", "TOTAL SUPERFICIE AFECTADA", "AÑO", "LATITUD", "LONGITUD"]]

  # Limpiar los datos, Eliminando los registros sin Comuna
  #data_comuna.dropna(subset=["COMUNA"], inplace=True)

  return incendios"""

# Obtener datos desde cache
data_puntos = data_incendio()
print(data_puntos)
# Generar listado de regin ordenados
region_puntos = data_puntos["REGION"].sort_values().unique()

# Generar listado de provincia ordenadas
provincia_puntos = data_puntos["PROVINCIA"].sort_values().unique()

# Generar listado de COMUNA ordenadas
comuna_puntos = data_puntos["COMUNA"].sort_values().unique()


with st.sidebar:
  st.write("##### Filtros de Información")
  st.write("---")

  # Multiselector de REGION
  region_sel = st.multiselect(
    label="Regiones",
    options=region_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not region_sel:
    region_sel = region_puntos.tolist()

  # Multiselector de PROVINCIA
  provincia_sel = st.multiselect(
    label="Provincia",
    options=provincia_puntos,
    default=provincia_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not provincia_sel:
    hora_sel = provincia_puntos.tolist()

# Multiselector de COMUNA
  comuna_sel = st.multiselect(
    label="Comuna",
    options=comuna_puntos,
    default=comuna_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comuna_puntos.tolist()



# Aplicar Filtros
incendios_data = data_puntos.query(" REGION==@region_sel and PROVINCIA==@provincia_sel and COMUNA==@comuna_sel")

if incendios_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_lat = np.median(incendios_data["LATITUD"])
  avg_lng = np.median(incendios_data["LONGITUD"])

  puntos_mapa = pdk.Deck(
      map_style=None,
      initial_view_state=pdk.ViewState(
          latitude=avg_lat,
          longitude=avg_lng,
          zoom=10,
          min_zoom=10,
          max_zoom=15,
          pitch=20,
      ),
      layers=[
        pdk.Layer(
          "ScatterplotLayer",
          data=incendios_data,
          pickable=True,
          auto_highlight=True,
          get_position='[LONGITUD, LATITUD]',
          filled=True,
          opacity=0.6,
          radius_scale=10,
          radius_min_pixels=3,
          #get_fill_color=["Horario == '08:30 - 18:30' ? 255 : 10", "Horario == '08:30 - 18:30' ? 0 : 200", 90, 200]
        )      
      ]
  )

  st.write(puntos_mapa)


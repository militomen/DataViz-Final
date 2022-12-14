import streamlit as st

import pydeck as pdk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",
  
)

@st.cache(allow_output_mutation=True)
def carga_data2():
  return pd.read_excel("ODC2022.xlsx") 

# Se lee la información de forma óptima
data_puntos = carga_data2()

# Generar listado de horarios ordenados
horarios_puntos = data_puntos["REGION"].sort_values().unique()

# Generar listado de comunas ordenadas
comunas_puntos = data_puntos["COMUNA"].sort_values().unique()

data_puntos.dropna(subset=["COMUNA"], inplace=True)
data_puntos.dropna(subset=["LATITUD"], inplace=True)
data_puntos.dropna(subset=["LONGITUD"], inplace=True)
data_puntos.dropna(subset=["NUMERO INCENDIOS "], inplace=True)

with st.sidebar:
  st.write("##### Filtros de Información")
  st.write("---")

  # Multiselector de comunas
  comuna_sel = st.multiselect(
    label="Comuna",
    options=comunas_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comunas_puntos.tolist()

  # Multiselector de horarios
  region_sel = st.multiselect(
    label="Region",
    options=horarios_puntos,
    default=horarios_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not region_sel:
    region_sel = horarios_puntos.tolist()



# Aplicar Filtros
geo_data = data_puntos.query(" REGION==@region_sel and COMUNA==@comuna_sel")

if geo_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_lat = np.median(geo_data["LATITUD"])
  avg_lng = np.median(geo_data["LONGITUD"])

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
          "HeatmapLayer",
          data=geo_data,
          pickable=True,
          auto_highlight=True,
          get_position='[LONGITUD, LATITUD]',
          opacity=0.6,
          get_weight="Horario == '10:00 - 14:00' ? 255 : 10"
        )       
      ],
      tooltip={
        "html": "<b>Region: </b> {REGION} <br /> "
                "<b>Provincia: </b> {PROVINCIA} <br /> "
                "<b>Comuna: </b> {COMUNA} <br /> "
                "<b>Georeferencia (Lat, Lng): </b>[{LATITUD}, {LONGITUD}] <br /> ",
        "style": {
          "backgroundColor": "steelblue",
          "color": "white"
        }
      }
  )

  st.write(puntos_mapa)
  st.write(geo_data)

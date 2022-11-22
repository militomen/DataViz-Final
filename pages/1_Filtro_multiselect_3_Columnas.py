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
    label="Comunas en Funcionamiento",
    options=comunas_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comunas_puntos.tolist()

  # Multiselector de horarios
  hora_sel = st.multiselect(
    label="Horario de Funcionamiento",
    options=horarios_puntos,
    default=horarios_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not hora_sel:
    hora_sel = horarios_puntos.tolist()

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"

col_bar, col_pie, col_table = st.columns(3, gap="large")

# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"

# Aplicar Filtros
geo_data = data_puntos.query(" REGION==@hora_sel and COMUNA==@comuna_sel")


if geo_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_lat = np.median(geo_data["LATITUD"])
  avg_lng = np.median(geo_data["LONGITUD"])
  group_comuna = geo_data.groupby(["COMUNA"]).size()
  group_comuna.sort_values(axis="index", ascending=False, inplace=True)

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
          data=geo_data,
          pickable=True,
          auto_highlight=True,
          get_position='[LONGITUD, LATITUD]',
          filled=True,
          opacity=0.6,
          radius_scale=10,
          radius_min_pixels=3,
          get_fill_color=["Horario == '08:30 - 18:30' ? 255 : 10", "Horario == '08:30 - 18:30' ? 0 : 200", 90, 200]
        )      
      ],
      tooltip={
        "html": "<b>Negocio: </b> {Negocio} <br /> "
                "<b>Dirección: </b> {Dirección} <br /> "
                "<b>Comuna: </b> {Comuna} <br /> "
                "<b>Horario: </b> {Horario} <br /> "
                "<b>Código: </b> {CODIGO} <br /> "
                "<b>Georeferencia (Lat, Lng): </b>[{LATITUD}, {LONGITUD}] <br /> ",
        "style": {
          "backgroundColor": "steelblue",
          "color": "white"
        }
      }
  )

  #st.write(puntos_mapa)

  with col_bar:
    bar = plt.figure()
    group_comuna.plot.bar(
      title="Cantidad de Puntos de Carga por Comuna",
      label="Total de Puntos",
      xlabel="Comunas",
      ylabel="Puntos de Carga",
      color="lightblue",
      grid=True,
    ).plot()
    st.pyplot(bar)

  with col_pie:
    pie = plt.figure()
    group_comuna.plot.pie(
      y="index",
      title="Cantidad de Puntos de Carga por Comuna",
      legend=None,
      autopct=formato_porciento
    ).plot()
    st.pyplot(pie)

  with col_table:
    pie = plt.figure()
    group_comuna.plot.line(
      title="Cantidad de Puntos de Carga por Comuna",
      label="Total de Puntos",
      xlabel="Comunas",
      ylabel="Puntos de Carga",
      color="lightblue",
      grid=True
    ).plot()
    st.pyplot(pie)

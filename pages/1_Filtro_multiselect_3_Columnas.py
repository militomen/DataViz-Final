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
    label="Comunas",
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

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"

col_bar, col_pie, col_table = st.columns(3, gap="large")

# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"

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
  group_comuna = geo_data.groupby(["COMUNA"]).size()
  group_comuna.sort_values(axis="index", ascending=False, inplace=True)

  with col_bar:
    bar = plt.figure()
    group_comuna.plot.bar(
      title="Cantidad de incendios por Comuna",
      label="Total de Puntos",
      xlabel="Comunas",
      ylabel="Incendios",
      color="lightblue",
      grid=True,
    ).plot()
    st.pyplot(bar)

  with col_pie:
    pie = plt.figure()
    group_comuna.plot.pie(
      y="index",
      title="Cantidad de incendios por Comuna",
      legend=None,
      autopct=formato_porciento
    ).plot()
    st.pyplot(pie)

  with col_table:
    pie = plt.figure()
    group_comuna.plot.line(
      title="Cantidad de incendios por Comuna",
      label="Total de incendios",
      xlabel="Comunas",
      ylabel="Incendios",
      color="lightblue",
      grid=True
    ).plot()
    st.pyplot(pie)

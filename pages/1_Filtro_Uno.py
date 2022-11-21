import streamlit as st

import pydeck as pdk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Se importan funcionalidades desde librería propia
#from utils import data_incendio

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",
  
)

@st.cache
def data_incendio():
  return pd.read_excel("ODC2022.xlsx")  
# Obtener datos desde cache
data_puntos = data_incendio()
# Generar listado de regin ordenados
region_puntos = data_puntos["REGION"].sort_values().unique()

# Generar listado de provincia ordenadas
provincia_puntos = data_puntos["PROVINCIA"].sort_values().unique()

# Generar listado de COMUNA ordenadas
comuna_puntos = data_puntos["COMUNA"].sort_values().unique()


datoscomuna = data_puntos[['COMUNA', 'NUMERO INCENDIOS ']]
datoscomuna.dropna(subset=["NUMERO INCENDIOS "], inplace=True)
print(datoscomuna)

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
    default=None
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not provincia_sel:
    hora_sel = provincia_puntos.tolist()

# Multiselector de COMUNA
  comuna_sel = st.multiselect(
    label="Comuna",
    options=comuna_puntos,
    default=None
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comuna_puntos.tolist()

col_bar, col_pie, col_line = st.columns(3, gap="small")

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"

with col_bar:
  bar = plt.figure()
  datoscomuna.plot.bar(
    title="Cantidad de Puntos de Carga por Comuna",
    label="Total de Puntos",
    xlabel="Comunas",
    ylabel="Puntos de Carga",
    color="lightblue",
    grid=True,
  ).plot()
  st.pyplot(bar)

# Aplicar Filtros
incendios_data = data_puntos.query(" REGION==@region_sel and PROVINCIA==@provincia_sel and COMUNA==@comuna_sel")

if incendios_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  #avg_lat = np.median(incendios_data["LATITUD"])
  #avg_lng = np.median(incendios_data["LONGITUD"])
  st.warning("#### se deberian mostrar registros!!!")

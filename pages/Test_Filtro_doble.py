import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",
  
)

@st.cache(allow_output_mutation=True)
def carga_data3():
  return pd.read_excel("ODC2022.xlsx") 

# Se lee la información de forma óptima
bip = carga_data3()

st.header("Challenge de Visualizaciones")
st.info("##### Top 5 de Puntos de Carga por Comuna")

# Ya se pueden obtener los 5 primeros registros

region_puntos = bip["REGION"].sort_values().unique()

provincia_puntos = bip["PROVINCIA"].sort_values().unique()


group_comuna = bip.groupby(["COMUNA"]).size()
# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"
group_comuna.sort_values(axis="index", ascending=False, inplace=True)

bip.dropna(subset=["COMUNA"], inplace=True)
bip.dropna(subset=["LATITUD"], inplace=True)
bip.dropna(subset=["LONGITUD"], inplace=True)
bip.dropna(subset=["NUMERO INCENDIOS "], inplace=True)

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"


################################################################################################
st.info("##### Agrupación Puntos de Carga por Comuna")

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
    provincia_sel = provincia_puntos.tolist()


# Obtener parte de la información
col_bar, col_pie, col_table = st.columns(3, gap="large")


#print(geo_data)

geo_data = bip.query(" REGION==@region_sel and PROVINCIA==@provincia_sel")

# Aplicar filtro de Comuna
if geo_data.empty:
  # Advertir al usuario que no hay datos para los filtros
    st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  #avg_lat = np.median(incendios_data["LATITUD"])
  #avg_lng = np.median(incendios_data["LONGITUD"])
    st.warning("#### se deberian mostrar registros!!!")
    with col_bar:
      bar = plt.figure()
      geo_data.plot.bar(
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
      geo_data.plot.pie(
          y="index",
          title="Cantidad de Puntos de Carga por Comuna",
          legend=None,
          autopct=formato_porciento
      ).plot()
    st.pyplot(pie)

    with col_table:
      pie = plt.figure()
      geo_data.plot.line(
          title="Cantidad de Puntos de Carga por Comuna",
          label="Total de Puntos",
          xlabel="Comunas",
          ylabel="Puntos de Carga",
          color="lightblue",
          grid=True
      ).plot()
    st.pyplot(pie)

import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",
  
)

@st.cache
def carga_data1():
  return pd.read_excel("ODC2022.xlsx") 

# Se lee la información de forma óptima
bip = carga_data1()

st.header("Challenge de Visualizaciones")
st.info("##### Top 5 de Puntos de Carga por Comuna")

################################################################################################
col_bar, col_pie, col_table = st.columns(3, gap="large")
# Agrupar los datos, en base a la columna donde están las comunas
# Se genera la serie de la agrupación usando "size()"
group_comuna = bip.groupby(["COMUNA"]).size()
# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"
group_comuna.sort_values(axis="index", ascending=False, inplace=True)
# Ya se pueden obtener los 5 primeros registros
top5 = group_comuna

print(top5)

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"

with col_bar:
  bar = plt.figure()
  top5.plot.bar(
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
  top5.plot.pie(
    y="index",
    title="Cantidad de Puntos de Carga por Comuna",
    legend=None,
    autopct=formato_porciento
  ).plot()
  st.pyplot(pie)

with col_table:
  pie = plt.figure()
  top5.plot.line(
    title="Cantidad de Puntos de Carga por Comuna",
    label="Total de Puntos",
    xlabel="Comunas",
    ylabel="Puntos de Carga",
    color="lightblue",
    grid=True
  ).plot()
  st.pyplot(pie)

################################################################################################
st.info("##### Agrupación Puntos de Carga por Comuna")

col_sel, col_map = st.columns([1,2])

# Crear grupos por cantidad de puntos
group_20 = group_comuna.apply(lambda x: x if x <= 20 else None).dropna(axis=0)
group_60 = group_comuna.apply(lambda x: x if x > 20 and x <= 60 else None).dropna(axis=0)
group_max = group_comuna.apply(lambda x: x if x > 60 else None).dropna(axis=0)


with col_sel:
  pie = plt.figure()
  top5.plot.line(
    title="Cantidad de Puntos de Carga por Comuna",
    label="Total de Puntos",
    xlabel="Comunas",
    ylabel="Puntos de Carga",
    color="lightblue",
    grid=True
  ).plot()
  st.pyplot(pie)


# Obtener parte de la información

bip.dropna(subset=["COMUNA"], inplace=True)
bip.dropna(subset=["LATITUD"], inplace=True)
bip.dropna(subset=["LONGITUD"], inplace=True)
bip.dropna(subset=["NUMERO INCENDIOS "], inplace=True)
geo_data = bip

print(geo_data)


with col_map:
  bar = plt.figure()
  top5.plot.bar(
    title="Cantidad de Puntos de Carga por Comuna",
    label="Total de Puntos",
    xlabel="Comunas",
    ylabel="Puntos de Carga",
    color="lightblue",
    grid=True,
  ).plot()
  st.pyplot(bar)


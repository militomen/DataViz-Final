import streamlit as st
import pandas as pd


@st.cache
def data_incendio():
  # Se lee Excel de datos
  incendios=pd.read_excel("ODC2022.xlsx")

  # Obtener columnas de datos
 # data_comuna = incendios[ ["REGION","PROVINCIA", "COMUNA", "NUMERO INCENDIOS ", "TOTAL  FORESTAL ", "TOTAL OTRAS SUPERFICIES", "TOTAL SUPERFICIE AFECTADA", "AÑO", "LATITUD", "LONGITUD"]]

  # Limpiar los datos, Eliminando los registros sin Comuna
  #data_comuna.dropna(subset=["COMUNA"], inplace=True)

  return incendios

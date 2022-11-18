import streamlit as st
import pandas as pd

# Se crea lista de horarios de funcionamiento
# esta información puede venir desde otro Excel, CSV o API

horarios = [
  "08:00 - 18:00",
  "13:00 - 17:00",
  "08:30 - 18:30",
  "09:30 - 19:30",
  "10:00 - 14:00",
  "12:00 - 16:00",
]


def asigna_horario(data):
  comuna=data["Comuna"]
  latitud=data["LATITUD"]

  if(latitud < -33.49):
    return horarios[5]
  elif(comuna=="RENCA" and latitud < -33.51):
    return horarios[0]
  elif(comuna=="RENCA"):
    return horarios[1]
  elif(comuna=="PROVIDENCIA"):
    return horarios[2]
  elif(comuna=="HUECHURABA"):
    return horarios[3]
  else:
    return horarios[4]


@st.cache
def geo_data():
  # Se lee Excel de datos
  bip=pd.read_excel("carga-bip.xlsx", header=9)

  # Obtener columnas de datos
  data_comuna = bip[ ["CODIGO","NOMBRE FANTASIA", "CERRO BLANCO 625", "MAIPU", "LATITUD", "LONGITUD", "HORARIO REFERENCIAL"]]

  # Corregir los nombres de las columnas
  geo_data_comuna = data_comuna.rename(columns={
    "NOMBRE FANTASIA": "Negocio", 
    "CERRO BLANCO 625": "Dirección", 
    "MAIPU": "Comuna",
    "HORARIO REFERENCIAL": "Horario"
  })

  # Limpiar los datos, Eliminando los registros sin Comuna
  geo_data_comuna.dropna(subset=["Comuna"], inplace=True)

  # Asignar valores de horarios a la columna de Horario,
  # para esto se aplica una lógica usando todas las columnas de cada registro
  geo_data_comuna["Horario"] = geo_data_comuna.apply(asigna_horario, axis=1)

  return geo_data_comuna

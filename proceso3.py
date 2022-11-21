"""3. Publicar la entrega, usando:

- Publicar el repositorio en GitHub con todos los archivos del proyecto.
	2 Puntos
- Publicar la aplicación en línea, mediante el servicio gratuito de Stremlit Cloud y personalizar el subdominio
	3 Puntos
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

incendios=pd.read_excel("ODC2022.xlsx")

datoscomuna = incendios[['COMUNA', 'NUMERO INCENDIOS ']]
print(datoscomuna)

bar = plt.figure()

datoscomuna.plot(
	title="Cantidad de Puntos de Carga por Comuna",
	label="Total de Puntos",
	xlabel="Comunas",
	ylabel="Puntos de Carga",
	color="lightblue",
	grid=True,
)
plt.show()
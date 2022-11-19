import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from sqlalchemy import Column, Float, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, Session

#- Usar un archivo Excel como fuente de datos iniciales, con al menos 1000 registros. Puede ser un archivo propio o bien obtenido de alguna fuente pública, de cualquier forma, debe quedar disponible en el repositorio de entrega.
def carga_inicial():
  return pd.read_excel("ODC2022.xlsx")

odc = carga_inicial()

# Modificar algunos nombres de columnas de datos, independiente a que sean correctos, lo que se espera es la capacidad de cambiar sus nombres.
odc_renombrado = odc.rename(columns={'TOTAL  FORESTAL':'AREA FORESTAL AFECTADA',
                                   'TOTAL OTRAS SUPERFICIES':'OTRAS AREAS AFECTADAS',
                                   'TOTAL SUPERFICIE AFECTADA':'AREA TOTAL AFECTADA'})

#- Crear una columna de datos en el DataFrame, con la siguiente definición: “Fecha de Proceso”, 
# donde se debe registrar la fecha en que se está procesando el Excel. Tip: La misma fecha para
#  todos los registros en esa columna.
fecha_actual = datetime.datetime.now()
odc_renombrado['Fecha de Proceso'] = fecha_actual.strftime("%d-%m-%Y")

#- Crear una columna vacía en el DataFrame con el nombre “Clima”, después asignarle 
# valor de clima obtenido desde API de OpenWeatherMap, para esto aplicar una lógica 
# a elección propia, donde se evalúen al menos 2 columnas y el dato debe provenir de
#  al menos 5 comunas. Tip: se debe hacer la consulta de las 5 comunas antes de aplicar
#  el dato a la columna de Clima, similar al ejemplo de horarios en la clase final.
odc_renombrado['Clima'] = ("")
#Obtener lista de comunas resumidas
comunas = odc_renombrado["COMUNA"].sort_values().unique()

#Agrupar y sumar por la columna NUMERO DE INCENDIOS
agrupado = odc_renombrado.groupby(['COMUNA']).agg(
                                  {'NUMERO INCENDIOS ': 'sum'  
                                   #'Clima':'sum' 
                                   #'ultima_visita':'max'
                                  }).reset_index().sort_values(by="NUMERO INCENDIOS ", ascending=False)
print(agrupado)
agrupado['Clima'] = ("")
#top5 = agrupado ['COMUNA']
top5 = [agrupado[0:5]]

#Aplicar a la columna clima Segun el top 5 y la cantidad de incendios
#Riesgo Alto, Medio, Bajo 

def asigna_clima(agrupado):
  comuna=agrupado["COMUNA"]
  incendios=agrupado["NUMERO INCENDIOS "]

  if(comuna=="Los Alamos" and incendios > 500):
    return "Riesgo Alto"
  elif(comuna=="COLLIPULLI" and incendios > 500):
    return "Riesgo Alto"
  elif(comuna=="CURANILAHUE"):
    return "Riesgo Alto"
  elif(comuna=="LEBU"):
    return "Riesgo Alto"
  elif(incendios > 700):
    return "Riesgo Probable"
  elif(incendios > 500):
    return "Riesgo Medio"
  elif(incendios > 300):
    return "Riesgo Considerable"
  elif(incendios > 100):
    return "Riesgoso"
  else:
    return "Riesgo muy bajo"


  # Limpiar los datos, Eliminando los registros sin Comuna
agrupado.dropna(subset=["COMUNA"], inplace=True)


  # Asignar valores de horarios a la columna de Horario,
  # para esto se aplica una lógica usando todas las columnas de cada registro
agrupado["Clima"] = agrupado.apply(asigna_clima, axis=1)
print(agrupado)
#- El DataFrame resultante, debe ser almacenado en una base de datos local
ruta_mi_bd = os.path.abspath("./incendios.db")
mi_bd = f"sqlite:///{ruta_mi_bd}"

engine = create_engine(mi_bd, echo=True, future=True)
# Crear clase de Modelo de Datos SQLAlchemy
Base = declarative_base()

# Crear clase de Modelo de la tabla a usar
class CargasIncendios(Base):
  # Nombre de la tabla
  __tablename__ = "cargasincendios"

  # Definir cada atributo de la tabla y su tipo de dato
  COMUNA = Column(String(100), primary_key=True)
  NUMERO_INCENDIOS = Column(Integer)
  CLIMA = Column(String(100))

  def __repr__(self) -> str:
    return f" CargasIncendios(COMUNA={self.COMUNA}, NUMERO_INCENDIOS={self.NUMERO_INCENDIOS}, CLIMA={self.CLIMA}, " \
      + ")"

# Crear la tabla en BD
Base.metadata.create_all(engine)

# Corregir nombres de columnas
agrupado.rename(columns={
  "NUMERO INCENDIOS": "NUMERO_INCENDIOS",
}, inplace=True)
# Grabar DataFrame en BD
agrupado.to_sql(con=engine, name="cargasincendios", if_exists="replace", index_label="COMUNA")

# Crear sesión a BD
session = Session(engine)

# Consultar por registros de algunas comunas
"""sql_comuna = select(CargasIncendios).where(CargasIncendios.COMUNA.in_(["RENCA", "ÑUÑOA"]) )
registros_comuna = session.scalars(sql_comuna).all()
for punto_carga in registros_comuna:
  print(punto_carga)
"""

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"

#- Obtener los registros de la base de datos y exportar a un nuevo archivo Excel y otro archivo CSV.



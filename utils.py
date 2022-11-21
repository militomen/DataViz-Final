import streamlit as st
import pandas as pd


@st.cache
def data_incendio():
  incendios=pd.read_excel("ODC2022.xlsx")
  return incendios

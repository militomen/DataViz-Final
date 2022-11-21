import streamlit as st
import streamlit.components.v1 as components

# Se configura la página
st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",
  
)


st.sidebar.write("## Visualizacion de datos")

st.write("### TRABAJO FINAL")

components.html("""
  <iframe width="100%" height="520" 
    src="https://www.youtube-nocookie.com/embed/O5Wc0p9tSzw?modestbranding=1&controls=0&auto=1"
    title="TRABAJO FINAL" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>
""", height=520)

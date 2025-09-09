import streamlit as st
import pandas as pd
import fnmatch
import requests

# Descargar el archivo desde Google Sheets
sheet_id = "1Hwp5cYXLJn8kptOEPNxS3I-Mp98wHNkV"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
response = requests.get(url)
with open("google_sheet.xlsx", "wb") as f:
    f.write(response.content)

# Cargar el archivo Excel
df = pd.read_excel("google_sheet.xlsx", engine="openpyxl")

# Configuración de la página
st.set_page_config(page_title="Buscador Almacén MS", layout="wide")
st.title("🔍 Buscador Almacén MS")
st.markdown("Escribe un texto con (*)")

# Campo de búsqueda
query = st.text_input("Buscar", placeholder="Ejemplo: sonda*temper*")

# Procesar búsqueda
if query:
    query = query.lower()
    filtered_rows = []
    for _, row in df.iterrows():
        if any(fnmatch.fnmatch(str(cell).lower(), query) for cell in row):
            filtered_rows.append(row)

    # Mostrar resultados
    if filtered_rows:
        st.success(f"Se encontraron {len(filtered_rows)} coincidencias.")
        st.dataframe(pd.DataFrame(filtered_rows, columns=df.columns))
    else:
        st.warning("No se encontraron coincidencias.")
else:
    st.info("Introduce un texto para buscar.")

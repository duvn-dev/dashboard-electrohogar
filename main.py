import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard ElectroHogar", layout="wide")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("T3_VW_CuboVentas.csv") 
    df.columns = df.columns.str.upper()
    return df

df = pd.read_csv("T3_VW_CuboVentas.csv", encoding='latin1')

st.title("Dashboard de Ventas - ElectroHogar S.A.S.")
st.write("Análisis del Cubo Lógico de Ventas - Proyecto Tecnologías ETL (UNAD)")

st.sidebar.header("Filtros de Búsqueda")

regiones = df['REGION'].unique().tolist()
regiones.insert(0, "Todas")
region_seleccionada = st.sidebar.selectbox("Seleccione una Región", regiones)

if region_seleccionada != "Todas":
    df_filtrado = df[df['REGION'] == region_seleccionada]
else:
    df_filtrado = df.copy()

mes_min = int(df_filtrado['MES'].min())
mes_max = int(df_filtrado['MES'].max())
meses_seleccionados = st.sidebar.slider(
    "Seleccione el rango de Meses", 
    min_value=mes_min, 
    max_value=mes_max, 
    value=(mes_min, mes_max)
)

df_filtrado = df_filtrado[(df_filtrado['MES'] >= meses_seleccionados[0]) & (df_filtrado['MES'] <= meses_seleccionados[1])]

st.subheader("Métricas Generales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Ventas", f"${df_filtrado['TOTALVENTA'].sum():,.2f}")
with col2:
    st.metric("Cantidad Vendida", f"{df_filtrado['CANTIDADVENDIDA'].sum():,.0f}")
with col3:
    st.metric("Costo Total", f"${df_filtrado['COSTOTOTAL'].sum():,.2f}")
with col4:
    st.metric("Margen Total", f"${df_filtrado['MARGENTOTAL'].sum():,.2f}")

st.divider()

col_grafico, col_tabla = st.columns([3, 2])

with col_grafico:
    st.subheader("Margen Total por Subcategoría")
    df_grafico = df_filtrado.groupby('SUBCATEGORIA')['MARGENTOTAL'].sum().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df_grafico.index, df_grafico.values, color='#1f77b4')
    ax.set_xlabel("Margen Total ($)")
    ax.set_ylabel("Subcategoría")
    
    st.pyplot(fig)

with col_tabla:
    st.subheader("Datos Detallados")
    st.dataframe(df_filtrado[['MES', 'CIUDAD', 'SUBCATEGORIA', 'TOTALVENTA', 'MARGENTOTAL']], use_container_width=True)
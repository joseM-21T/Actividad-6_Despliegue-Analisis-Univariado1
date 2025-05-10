# Importamos librerías
import streamlit as st 
import plotly.express as px
import pandas as pd

# Aplicar estilos personalizados en el sidebar
st.markdown("""
    <style>
        /* Estilo para el sidebar */
        [data-testid="stSidebar"] {
            background-color: turquoise !important;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
### Carga de datos 
def load_data():
    df = pd.read_csv("Wuppi convertido.csv")
    Lista = ["Administrador", "botón correcto", "mini juego", "color presionado", "dificultad", "Juego", 
             "auto push", "tiempo de interacción", "tiempo de lección", "tiempo de sesión"]
    return df, Lista

df, Lista = load_data()



# Columnas para distribuir contenido
col1, col2 = st.columns([1, 4])
with col1:
    st.image("foto.png", width=150)

# Lista de usuarios válidos
usuarios_validos = [1, 3, 27, 8]

# Selección del usuario en sidebar
Usuario_Seleccionado = st.sidebar.selectbox(
    label="Selecciona un usuario",
    options=usuarios_validos,
    index=0
)

# Filtrar datos según usuario
df_filtrado = df[df['Usuario'] == Usuario_Seleccionado]

# Selector análisis
st.sidebar.image("foto2.png", width=150)
View = st.sidebar.selectbox(
    label="Tipo de análisis", 
    options=["Extracción de características", "Regresión Lineal", "Regresión No Lineal", "Regresión Logística", "Anova","Diccionario"]
)

if View == "Extracción de características":
    # Opciones de variables
    todas_las_variables = ["Seleccionar todos"] + Lista
    variables_seleccionadas = st.sidebar.multiselect(
        label="Selecciona las variables a analizar",
        options=todas_las_variables,
        default=["Seleccionar todos"]
    )
    if "Seleccionar todos" in variables_seleccionadas:
        variables_seleccionadas = Lista
    
    st.title("Extracción de características")
    
    variables_barras = ["botón correcto", "mini juego", "color presionado", "auto push", "Juego"]
    
    paleta_colores = {
        1: ["lightcoral", "indianred", "firebrick"],
        3: ["lightblue", "dodgerblue", "navy"],
        27: ["lightgreen", "mediumseagreen", "forestgreen"],
        8: ["plum", "mediumorchid", "darkmagenta"]
    }
    
    for Variable_Cat in variables_seleccionadas:
        # Filtrar si la variable es tiempo y tiene valores >0
        if Variable_Cat in ["tiempo de lección", "tiempo de sesión"]:
            df_filtrado_variable = df_filtrado[df_filtrado[Variable_Cat] > 0]
        else:
            df_filtrado_variable = df_filtrado

        # Validar si la columna existe y tiene datos
        if Variable_Cat not in df_filtrado_variable.columns or df_filtrado_variable.empty:
            st.warning(f"La columna {Variable_Cat} no tiene datos válidos o no existe.")
            continue

        # Count y filtrado de categorías
        Tabla_frecuencias = df_filtrado_variable[Variable_Cat].value_counts().reset_index()
        Tabla_frecuencias.columns = ["categorias", "frecuencia"]
        if Variable_Cat in ["botón correcto", "mini juego", "color presionado"]:
            Tabla_frecuencias = Tabla_frecuencias[Tabla_frecuencias["categorias"] != 99]
        
        st.subheader(f"Análisis de {Variable_Cat}")

        colores_usuario = paleta_colores.get(Usuario_Seleccionado, ["gray"])
        
        Contenedor_A, Contenedor_B = st.columns(2)
        
        with Contenedor_A:
            if Variable_Cat in ["tiempo de lección", "tiempo de sesión"] or Variable_Cat in variables_barras:
                st.write("Gráfico de barras")
                fig_bar = px.bar(
                    data_frame=Tabla_frecuencias,
                    x="categorias",
                    y="frecuencia",
                    title=f"Frecuencia por categoría: {Variable_Cat}",
                    color_discrete_sequence=colores_usuario
                )
                fig_bar.update_layout(height=300)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.write("Gráfico de área")
                fig_area = px.area(
                    data_frame=Tabla_frecuencias,
                    x="categorias",
                    y="frecuencia",
                    title=f"Frecuencia por categoría: {Variable_Cat}",
                    color_discrete_sequence=colores_usuario
                )
                fig_area.update_layout(height=300)
                st.plotly_chart(fig_area, use_container_width=True)
        with Contenedor_B:
            if Variable_Cat not in ["tiempo de lección", "tiempo de sesión"]:
                st.write("Gráfico de pastel")
                fig_pie = px.pie(
                    data_frame=Tabla_frecuencias,
                    names="categorias",
                    values="frecuencia",
                    title=f"Frecuencia por categoría: {Variable_Cat}",
                    color_discrete_sequence=colores_usuario
                )
                fig_pie.update_layout(height=300)
                st.plotly_chart(fig_pie, use_container_width=True)

elif View == "Diccionario":
    st.write("Diccionario de extracción de características")
    st.write("Usuarios: 1:Leonardo, 3:Nicolas, 8:Sergio Angel, 27:Rene")
    st.write("Administrador: 1:Aleida, 2:Nicolas, 3:Leonardo, 4:Dennis, 5:Sergio Angel, 6:Carlos E, 7:Yael D, 8:Austin, 9:Valentin, 10:Erick, 11:Iker B, 12:Kytzia, 13:Benjamin")
    st.write("boton correcto: 0:Boton incorrecto 1:Boton correcto")
    st.write("Mini Juego: 1:Asteroides, 2:Restaurante, 3:Estrellas, 4:Gusanos, 5:Sonidos y animales, 6:Animales y colores, 7: Figuras y colores, 8:Partes del cuerpo, 9:Despegue, 10:Mini Game 0, 11:Mini Game 1, 12:Mini Game 2, 13: Mini Game 3")
    st.write("Color presionado: 1:Violeta, 2:Verde, 3:Amarillo, 4:Azul, 5:Rojo")
    st.write("dificultad: Episodio 1 ,Episodio 2, Episodio 3, Episodio 4")
    st.write("Juego 1:Astro, 2:Cadetes")
    st.write("Auto push: 0:No se presionó 1:Se presionó el Auto Push")
    

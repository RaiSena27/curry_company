import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)

# image_path = ('image_path.jpg')
image = Image.open('image_path.jpg')
st.sidebar.image(image, width=400)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard ")

st.markdown(
    """ 
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - Time de Data Science no Discord
        - @meigarom               
   """)
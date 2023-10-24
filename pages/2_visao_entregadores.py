# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime
import folium

from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Entregadores',
                   page_icon='🚚', layout='wide')

# -----------------------------------------------------
# Funções
# -----------------------------------------------------


def top_delivers(df1, top_asc):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
           .groupby(['City', 'Delivery_person_ID'])
           .max()
           .sort_values(['City', 'Time_taken(min)'], ascending=top_asc)
           .reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]
                    ).reset_index(drop=True)

    return df3


def clean_code(df1):
    """ Esta funcao tem a responsabilidade de limpar o dataframe

         Tipos de Limpeza:
         1. Removação dos dados NaN
         2. Mudança do tipo da coluna de dados
         3. Removação dos espaços das variáveis de texo
         4. Formatação da coluna de datas
         5. Limpeza da coluna de tempo ( remoção do texo da vareável numérica )

         Input: Dataframe
         Output: Dataframe

    """
    # 1. Convertendo a colula Age de texto para numeros inteiros ( int )
    linhas_vazias = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_vazias, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    linhas_vazias = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_vazias, :].copy()

    linhas_vazias = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_vazias, :].copy()

    linhas_vazias = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_vazias, :].copy()

    # 2. Conversao de texto/categoria/strings para numeros decimais ( float )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(
        float)

    # 3. Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 4. Convertendo a colula multiple_deliveries de texto para numeros inteiros
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 6. Comando para remover os espaços dentro de strings/texto/objct
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:,
                                                 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # 7. Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(
        lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


# -------------------------- Inicio da Estrutura Lógica do Código -------------------------------
# --------------------------
# Import Dataset
# --------------------------
df = pd.read_csv('dataset/train.csv')

# --------------------------
# Limpando os Dados
# --------------------------
df1 = clean_code(df)

# =================================================
# Barra Lateral
# =================================================
st.header('Marketplace - Visão Entregadores')

image_path = ('image_path.jpg')
image = Image.open(image_path)
st.sidebar.image(image, width=400)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data Limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

st.header(date_slider)
st.sidebar.markdown("""---""")


traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comudidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

st.dataframe(df1)

# =================================================
# Layout no Streamlit
# =================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.markdown('# Overall Matrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            # A maior idade dos entregadores
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior de idade', maior_idade)

        with col2:
            # A menor idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor de idade', menor_idade)
        with col3:
            # A melhor condição de veículo
            melhor_codicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_codicao)
        with col4:
            # A pior condição de veículos
            pior_codicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior Condição', pior_codicao)

    with st.container():
        st.markdown("""___""")
        st.title('Avaliacoes')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliacao media por Entregador')
            df_avg_ratings_per_deliver = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                             .groupby('Delivery_person_ID')
                                             .mean()
                                             .reset_index())
            st.dataframe(df_avg_ratings_per_deliver)

        with col2:
            st.markdown('##### Avaliacao media por transito')
            df_avg_std_ratings_by_traffic = (df1.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']]
                                                .groupby('Road_traffic_density')
                                                .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            # Mudança de nome das colunas
            df_avg_std_ratings_by_traffic.columns = [
                'delivery_mean', 'delivery_std']
            st.dataframe(df_avg_std_ratings_by_traffic)

            # Reset do index
            df_avg_std_ratings_by_traffic = df_avg_std_ratings_by_traffic.reset_index()

            st.markdown('##### Avaliacao media por clima')
            df_avg_std_ratings_by_weather = (df1.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']]
                                                .groupby('Weatherconditions')
                                                .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            # Mudança de nome das colunas
            df_avg_std_ratings_by_weather.columns = [
                'delivery_mean', 'delivery_std']

            # Reset do index
            df_avg_std_ratings_by_weather = df_avg_std_ratings_by_weather.reset_index()

            st.dataframe(df_avg_std_ratings_by_weather)

    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Top Entregadores Mais Rapidos')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)

        with col2:
            st.markdown('##### Top Entregadores Mais Lentos')
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)

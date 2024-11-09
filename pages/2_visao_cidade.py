from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image
import pandas as pd
import plotly.express as px
import numpy as np
import inflection
import streamlit as st

st.set_page_config(page_title='Visão Cidade', page_icon='🗾', layout='wide')

df1 = pd.read_csv('zomato.csv')

df = df1.copy()

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}


def country_name(country_id):
    return COUNTRIES[country_id]


def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]


def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


df['Country'] = df['Country Code'].apply(country_name)
df['Price tag'] = df['Price range'].apply(create_price_tye)
df['Color name'] = df['Rating color'].apply(color_name)



def process_cuisines(value):
    if isinstance(value, str):  # Se for uma string, converta para lista
        return [item.strip() for item in value.split(',')]
    elif isinstance(value, list):  # Se já for uma lista, apenas retorne
        return value
    else:
        return []  # Para outros tipos (como int, float, etc.), retorne uma lista vazia

# Aplicar a função para garantir que 'cuisines_list' tenha sempre listas válidas
df['cuisines_list'] = df['Cuisines'].apply(process_cuisines)



df = rename_columns(df)


# ===================================================================
# Barra Lateral
# ===================================================================

st.header("Fome Zero - Visão Cidade", divider=True)


image_path = 'tec.jpg'
image = Image.open( image_path )
st.sidebar.image(image, width=120)


st.sidebar.markdown('# Fome Zero Company')
st.sidebar.markdown('# Restaurants all the World')
st.sidebar.markdown("""---""")


#Escolher pais
country_options = st.sidebar.multiselect(
    'Filtro por pais',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']
)




st.sidebar.markdown("""---""")

#entrega online?

delivery_options_map = {1: 'Sim', 0: 'Não'}
entrega_online_options = st.sidebar.multiselect(
    'Entrega Online?',
    options=[delivery_options_map[1], delivery_options_map[0]],  
    default=[delivery_options_map[1], delivery_options_map[0]]    
)
entrega_online_options = [key for key, value in delivery_options_map.items() if value in entrega_online_options]

st.sidebar.markdown("""---""")

#price tag


tag_options = st.sidebar.multiselect(
    'Filtro por tag do preço',
    ['expensive', 'gourmet', 'normal', 'cheap'],
    default=['expensive', 'gourmet', 'normal', 'cheap']
)


st.sidebar.markdown("""---""")


#aceita reserva
reserva_options_map = {1: 'Sim', 0: 'Não'}
reserva_options = st.sidebar.multiselect(
    'Possui Reserva?',
    options=[reserva_options_map[1], reserva_options_map[0]],  
    default=[reserva_options_map[1], reserva_options_map[0]]    
)
reserva_options = [key for key, value in reserva_options_map.items() if value in reserva_options]


st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by Comunidade DS: Luigi Silva Ferrari')


linhas_selecionadas = df['country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]


linhas_selecionadas = df['has_online_delivery'].isin(entrega_online_options)
df = df.loc[linhas_selecionadas, :]


linhas_selecionadas = df['price_tag'].isin(tag_options)
df = df.loc[linhas_selecionadas, :]


linhas_selecionadas = df['has_table_booking'].isin(reserva_options)
df = df.loc[linhas_selecionadas, :]


st.dataframe(df.head())


# ===================================================================
# Layout no Streamlit
# ===================================================================


tab1, tab2 = st.tabs(['Visão Geral', '-'])

with tab1:
    with st.container():
        st.title("Overall Metrics")
        col1, col2, col3, col4, col5 = st.columns(5, gap='large')

        with col1:
            #Qtd restaurantes Registrados
            restaurantes_unicos = df['restaurant_id'].nunique()
            col1.metric('Restaurantes Registrados', restaurantes_unicos)
            
        with col2:
            #Qtd paises Registrados
            paises_unicos = df['country_code'].nunique()
            col2.metric('Paises Registrados', paises_unicos)
            
        with col3:
            #Qtd cidades Registrados
            cidade_unicas = df['city'].nunique()
            col3.metric('Cidades Registradas', cidade_unicas)     
            
        with col4:
            #Qtd avaliacoes
            avaliacoes_feitas = df['votes'].sum()
            col4.metric('Avaliações Registradas', avaliacoes_feitas)
            
        with col5:
            #Qtd culinaria Registrados
            tipo_culinaria = df['cuisines'].str.split(',').explode().str.strip().nunique()
            col5.metric('Culinaria Registradas', tipo_culinaria)


    with st.container():
        st.title('Cidade que possuem mais restaurantes')
        cidade_mais_restaurante = df.groupby('city')['restaurant_id'].nunique().reset_index()
        cidade_mais_restaurante = cidade_mais_restaurante.sort_values('restaurant_id', ascending=False)
        fig=px.bar(cidade_mais_restaurante, x='city', y='restaurant_id')
        st.plotly_chart(fig)


    with st.container():
        st.title('Cidade que possuem mais culinarias')
        culinarias_distintas_por_cidade = df.groupby('city')['cuisines_list'].apply(lambda x: pd.Series(x.sum()).nunique())
        graficoculinaria = culinarias_distintas_por_cidade.reset_index()
        graficoculinaria.columns = ['cidade', 'culinaria']
        graficoculinaria = graficoculinaria.sort_values('culinaria', ascending=False)
        fig = px.bar(graficoculinaria, x='cidade', y='culinaria')
        st.plotly_chart(fig)






























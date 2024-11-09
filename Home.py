import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)


image = Image.open('tec.jpg')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Fome Zero Company')
st.sidebar.markdown('# Fastested Delivery in Town')
st.sidebar.markdown("""---""")


st.sidebar.markdown('### Powered by Comunidade DS: Luigi Silva Ferrari')

st.markdown(
    """
        Bem-vindo ao Dashboard Fome Zero!

Aqui, você encontrará uma variedade de dados e gráficos importantes que fornecem uma visão abrangente sobre o desempenho dos restaurantes, além de informações consolidadas sobre o país e as cidades cadastradas. Esse painel foi projetado para facilitar sua análise e ajudar na tomada de decisões estratégicas.

No menu à esquerda, você poderá filtrar suas visualizações de acordo com:



 - País: escolha o país que deseja explorar;

 - Opções de entrega online: veja quais restaurantes oferecem essa modalidade;

 - Faixa de preço: filtre por tags de preço para comparar diferentes opções;

 - Reservas: verifique se o restaurante oferece opção de reserva.




Explore e aproveite ao máximo os dados disponíveis para aprimorar sua experiência e impulsionar seus objetivos no Fome Zero!


    """
)
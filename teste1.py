import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()

# Configuracao da pagina
st.set_page_config(layout="wide")

# st.title("Titulo da pagina")

st.markdown("# POC: Monitoramento COVID em Streamlit")
st.write("""Teste de criação de um painel de transparência de COVID-19 na cidade de Mogi Guaçu""")

# Importacao dos dados
sheet_id = "1SAg5J0YqGUXLHR6cGXhTT0UuMcx-npiEMWOslSm8N1A"
sheet_name = "covid19_atualizado"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

dados = pd.read_csv(url)


##################################################
# Processamento de dados

lista_mes_ano = []

for data in dados['data']:
    dia, mes, ano = data.split('/')
    lista_mes_ano.append("%d/%02d" %(int(ano), int(mes)))
dados['mes-ano'] = lista_mes_ano

##################################################

st.markdown("## Dados brutos")
st.write(dados)

# Configurando cards
st.markdown("# Indicadores")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric('Casos confirmados', dados[['casos_confirmados']].max(), delta=10, delta_color='inverse')
with c2:
    st.metric('Óbitos confirmados', dados[['obitos']].max(), delta=3)
with c3:
    st.metric('Ocupação máxima dos leitos de uti', dados[['leitos_uti_ocupados_covid19']].max(), delta=2, delta_color='inverse')

# Configurando layout: 2 colunas
st.markdown("## Gráficos")
col1, col2 = st.columns(2)

# Dados acumulados por mes-ano
dt_acumulado = dados.groupby('mes-ano').sum()[['novos_casos', 'novos_obitos']]

with col1:
    container1 = st.container()

    # Grafico 1
    container1.markdown("#### Novos casos por mês")
    dt_c1 = dt_acumulado[['novos_casos']]
    dt_c1['mes-ano'] = dt_c1.index

    container1.vega_lite_chart(dt_c1, spec={
        'height': 300,
        'mark': {'type': 'bar', 'tooltip': True, "cornerRadiusEnd": 5, 'color': '#311f89'},
        'encoding': {
            'x': {'field': 'mes-ano', 'type': 'nominal'},
            'y': {'field': 'novos_casos', 'type': 'quantitative', 'aggregate': 'sum'}
        },
    }, use_container_width=True)

with col2:
    container2 = st.container()

    # Grafico 2
    container2.markdown("#### Novos óbitos por mês")
    dt_c2 = dt_acumulado[['novos_obitos']]
    dt_c2['mes-ano'] = dt_c2.index

    container2.vega_lite_chart(dt_c2, {
        'height': 300,
        'mark': {'type': 'bar', 'tooltip': True, "cornerRadiusEnd": 5, 'color': 'red'},
        'encoding': {
            'x': {'field': 'mes-ano', 'type': 'nominal'},
            'y': {'field': 'novos_obitos', 'type': 'quantitative', 'aggregate': 'sum',
                  'axis': {
                      'grid': False}},
            'opacity': {'value': 1},
        },
    }, use_container_width=True)


# Dados maximos por mes-ano
dt_maximo = dados.groupby('mes-ano').max()[['novos_casos', 'novos_obitos', 'leitos_uti_ocupados_covid19', 'leitos_clinicos_ocupados']]
dt_maximo['mes-ano'] = dt_maximo.index

# Leitos hospitalares ocupados

tipo_leito = st.selectbox(label='Selecione o tipo de leito exibido', options=['UTI', 'Clínicos'])
dict_label_leitos = {'UTI': 'leitos_uti_ocupados_covid19', 'Clínicos': 'leitos_clinicos_ocupados'}

print(dt_maximo.dtypes)

st.vega_lite_chart(dt_maximo, {
        'height': 300,
        'mark': {'type': 'bar', 'tooltip': True, 'color': 'blue', "cornerRadiusEnd": 8},
        'encoding': {
            'x': {'field': 'mes-ano', 'type': 'nominal'},
            'y': {'field': dict_label_leitos[tipo_leito], 'type': 'quantitative',
                  'axis': {
                      'grid': False}},
            'opacity': {'value': 1},
        },
    }, use_container_width=True)






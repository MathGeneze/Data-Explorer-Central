import streamlit as st
import pandas as pd
import plotly.express as px

# --- CSS para adicionar GIF de fundo ---
# O bloco abaixo insere um GIF animado como fundo da aplicação usando CSS.
# Pode ser removido ou alterado conforme a identidade visual desejada.
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWZvcDV4azRiYjk2NmxhZG50OGZwcDc4YzJrcjR4MWc0OTJrdDkyciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dAWZiSMbMvObDWP3aA/giphy.gif');
        background-size: cover;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Cabeçalho da página ---
st.title('📚 Data Explorer Central')
st.subheader('Carregue seus dados. Explore estatísticas. Gere gráficos')
st.markdown('*Insira um **arquivo CSV** e explore as mais diversas estatísticas com **análise de gráficos**, **tabelas** e **métricas**.*')

# --- Upload de arquivo CSV ---
upload = st.file_uploader(
    label='Escolha um arquivo CSV:',
    type='CSV'
)

# --- Função para ler o CSV com cache ---
# O decorator @st.cache_data faz com que a função só execute novamente se o arquivo mudar,
# otimizando a performance da aplicação.

@st.cache_data
def carregar_csv(uploaded_file):
    """Lê o arquivo CSV enviado pelo usuário e retorna um DataFrame pandas."""
    return pd.read_csv(uploaded_file)


# --- Processamento do arquivo enviado ---
if upload is not None:
    try:
        tabela = carregar_csv(upload)
        st.success('Arquivo carregado com sucesso!', icon=':material/check:')
    except Exception as error:
        st.error(
            f'Erro ao ler o seu arquivo: {error}. Verifique se é um arquivo CSV válido.', icon=':material/close:')

# --- Exibição das primeiras linhas da tabela ---
if upload is not None:
    st.divider()
    st.subheader('🗂️ As primeiras linhas da sua tabela:')

    # Mostra a quantidade de colunas e linhas do arquivo carregado
    st.markdown(
        f'*Seu arquivo possui: **{len(tabela.columns)} colunas** e **{len(tabela.index)} linhas**.*')

    # Slider para o usuário escolher quantas linhas visualizar
    num_linhas = st.slider('Quantas linhas deseja visualizar?',
                           min_value=5, max_value=min(50, len(tabela)), value=5, step=1)
    st.dataframe(tabela.head(num_linhas))
    st.divider()

    # --- Visualização de colunas únicas ---
    st.subheader('📈 Visualização de Colunas Únicas')
    st.markdown('*Escolha entre colunas **Numéricas** e **Categóricas (texto)**. Visualize em formato de **gráfico de barras** e **métricas**.*')

    # Identifica colunas categóricas (texto) e numéricas
    colunas_categoricas = tabela.select_dtypes(exclude='number').columns
    colunas_numericas = tabela.select_dtypes(include='number').columns

    # Permite ao usuário escolher o tipo de coluna para análise
    escolha = st.selectbox(label='Qual tipo de coluna você gostaria de visualizar?', options=[
                           'Nenhuma', 'Numérica', 'Categórica'])

    if escolha is not None:

        # --- Gráfico para coluna categórica ---
        if escolha == 'Categórica':
            if len(colunas_categoricas) == 0:
                st.warning('Este arquivo não contém dados categóricos')
            
            else:
                coluna_barra = st.selectbox(
                'Selecione uma coluna categórica:', colunas_categoricas)

                # Exibe gráfico de barras com a contagem de cada categoria
                st.bar_chart(tabela[coluna_barra].value_counts())

        
        
        # --- Gráficos e métricas para coluna numérica ---
        if escolha == 'Numérica' and len(colunas_numericas) > 0:
            escolha_coluna_num = st.selectbox(
                'Selecione uma coluna numérica:', colunas_numericas)

            # Histograma da coluna numérica
            fig = px.histogram(tabela, x=escolha_coluna_num, nbins=20,
                               title=f'Histograma de {escolha_coluna_num}')
            st.plotly_chart(fig)

            # Boxplot da coluna numérica
            fig_box = px.box(tabela, y=escolha_coluna_num,
                             title=f'Boxplot de {escolha_coluna_num}')
            st.plotly_chart(fig_box)

            # --- Métricas estatísticas ---
            st.divider()
            st.subheader(
                f'🌐 Métricas da coluna: ▶︎ {escolha_coluna_num.title()} ◀︎ ')
            st.markdown(
                f'*Observe abaixo as métricas disponíveis da **coluna {escolha_coluna_num.title()}.***')

            # -- Métricas da coluna Superior
            maximo = tabela[escolha_coluna_num].max()
            minimo = tabela[escolha_coluna_num].min()
            soma = tabela[escolha_coluna_num].sum()
            media = tabela[escolha_coluna_num].mean()
            
            # -- Métricas da coluna Inferior
            contagem = tabela[escolha_coluna_num].count()
            moda = tabela[escolha_coluna_num].mode().loc[0]
            mediana = tabela[escolha_coluna_num].median()
            desvio_padrao = tabela[escolha_coluna_num].std()

            # Exibe as métricas em colunas para melhor visualização
            # -- Coluna supeior
            sup_col1, sup_col2, sup_col3, sup_col4 = st.columns(4)
            sup_col1.metric(label='Valor Máximo',value=f'{maximo}', border=True)
            sup_col2.metric(label='Valor Mínimo',value=f'{minimo}', border=True)
            sup_col3.metric(label='Soma', value=f'{soma}', border=True)
            sup_col4.metric(label='Média', value=f'{media}', border=True)
            
            # -- Coluna Inferior
            inf_col1, inf_col2, inf_col3, inf_col4 = st.columns(4)
            inf_col1.metric(label='Contagem de Valores',value=f'{contagem}', border=True)
            inf_col2.metric(label='Moda', value=f'{moda}', border=True)
            inf_col3.metric(label='Mediana', value=f'{mediana}', border=True)
            inf_col4.metric(label='Desvio Padrão',value=f'{desvio_padrao:.2f}', border=True)

    else:
        st.info('Nenhuma coluna categórica ou numérica disponível para gráfico.',
                icon=':material/warning:')

# --- Visualização de múltiplas colunas numéricas ---
if upload is not None and len(colunas_numericas) > 1:
    st.divider()
    st.subheader('📊 Visualização de Múltiplas Colunas')
    st.markdown(
        '*Selecione **duas colunas numéricas** e o **tipo de gráfico** para fazer análises comparativas.*')

    primeira_coluna = st.selectbox(
        label='Escolha a primeira coluna:', options=colunas_numericas)

    # Garante que há pelo menos outra coluna para comparar
    outras_colunas = colunas_numericas.drop(primeira_coluna)
    if len(outras_colunas) == 0:
        st.info('Não há outra coluna numérica para comparar.')
    else:
        segunda_coluna = st.selectbox(
            label='Escolha a segunda coluna:', options=outras_colunas)

        if primeira_coluna == segunda_coluna:
            st.warning('Selecione duas colunas diferentes!')
        else:
            escolha_grafico = st.selectbox(
                label='Selecione um tipo de gráfico:', options=['Nenhum', 'Barra', 'Linha', 'Área', 'Pizza', 'Dispersão', 'Caixa'])

            # Função para gerar diferentes tipos de gráficos comparativos
            @st.cache_data
            def gerar_grafico(df, coluna_x, coluna_y, tipo):
                if tipo == 'Barra':
                    fig = px.bar(df, x=coluna_x, y=coluna_y,
                                 title=f'Gráfico de Barra: {coluna_x} X {coluna_y}', color=primeira_coluna)
                elif tipo == 'Linha':
                    fig = px.line(df, x=coluna_x, y=coluna_y,
                                  title=f'Gráfico de Linha: {coluna_x} X {coluna_y}')
                elif tipo == 'Área':
                    fig = px.area(df, x=coluna_x, y=coluna_y,
                                  title=f'Gráfico de Área: {coluna_x} X {coluna_y}', color=primeira_coluna)
                elif tipo == 'Pizza':
                    fig = px.pie(
                        df, names=primeira_coluna, title=f"Gráfico de Pizza: Coluna - {primeira_coluna}.")
                    st.info(
                        'O gráfico de pizza não compara dados de 2 colunas! Altere as opções da 1ª coluna para visualizar os dados.', icon=':material/info:')
                elif tipo == 'Dispersão':
                    fig = px.scatter(
                        df, x=coluna_x, y=coluna_y, title=f"Gráfico de Dispersão: {coluna_x} X {coluna_y}", color=primeira_coluna)
                elif tipo == 'Caixa':
                    fig = px.box(df, x=coluna_x, y=coluna_y,
                                 title=f'Gráfico de Caixa: {coluna_x} X {coluna_y}')
                else:
                    fig = None
                return fig

            if escolha_grafico:
                fig = gerar_grafico(tabela, primeira_coluna,
                                    segunda_coluna, escolha_grafico)
                if fig:
                    st.plotly_chart(fig)

# --- Observações gerais ---
# - O código utiliza Streamlit para criar uma interface web interativa para análise de dados.
# - O usuário pode carregar um arquivo CSV, visualizar estatísticas e gráficos de suas colunas.
# - O uso de @st.cache_data otimiza a performance ao evitar recarregamento desnecessário dos dados.
# - O código está modularizado em blocos lógicos para facilitar manutenção e expansão.
# - Comentários explicativos foram adicionados para orientar futuros desenvolvedores.

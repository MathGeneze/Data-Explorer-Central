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
    type='csv'
)

# --- Função para ler o CSV com cache ---
# O decorator @st.cache_data faz com que a função só execute novamente se o arquivo mudar,otimizando a performance da aplicação.
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



# ------ Exibição das primeiras linhas da tabela ------
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



    # ------ Visualização de colunas únicas ------
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
                coluna_unica = st.selectbox(
                    'Selecione uma coluna categórica:', colunas_categoricas)
                
                
                # --- Usuário seleciona a posição do gráfico
                posicao = ['Vertical', 'Horizontal']
                c1, c2 = st.columns(2)
                opcoes = c1.pills('Escolha a posição do gráfico:', options=posicao)
                
                # --- Usuário pode selecionar a cor do gráfio
                escolha_cor = c2.color_picker("Escolha a cor do gráfico:", '#1585C1')
                
                if opcoes == 'Vertical':
                    # Exibe gráfico 
                    st.bar_chart(tabela[coluna_unica].value_counts(), horizontal=False, color=escolha_cor)
                else:
                    st.bar_chart(tabela[coluna_unica].value_counts(), horizontal=True, color=escolha_cor)


        # --- Gráficos e métricas para coluna numérica ---
        if escolha == 'Numérica' and len(colunas_numericas) > 0:
            escolha_coluna_num = st.selectbox(
                'Selecione uma coluna numérica:', colunas_numericas)

            # --- Usuário seleciona a posição do gráfico
            posicao = ['Vertical', 'Horizontal']
            c1, c2 = st.columns(2)
            opcoes = c1.pills('Escolha a posição do gráfico:', options=posicao)
            
            # --- Usuário pode selecionar a cor do gráfio
            escolha_cor = c2.color_picker("Escolha a cor do gráfico:", '#1585C1')
            
            if opcoes == 'Vertical':    
                 # Exibe gráfico 
                st.bar_chart(tabela[escolha_coluna_num].value_counts(), horizontal=False, color=escolha_cor)
            else:
                st.bar_chart(tabela[escolha_coluna_num].value_counts(), horizontal=True, color=escolha_cor)



        # ------ Métricas estatísticas ------ #
        st.divider()
        st.subheader(
            '🌐 Métricas Estatísticas ')
        st.markdown(
            f'*Observe abaixo as métricas disponíveis de cada **coluna numérica.***')

        escolha_metrica = st.selectbox('Selecione uma coluna:', colunas_numericas)
        
        # -- Métricas da coluna Superior
        maximo = tabela[escolha_metrica].max()
        minimo = tabela[escolha_metrica].min()
        soma = tabela[escolha_metrica].sum()
        media = tabela[escolha_metrica].mean()

        # -- Métricas da coluna Inferior
        contagem = tabela[escolha_metrica].count()
        moda = tabela[escolha_metrica].mode().loc[0]
        mediana = tabela[escolha_metrica].median()
        desvio_padrao = tabela[escolha_metrica].std()

        # Exibe as métricas em colunas para melhor visualização
        # -- Coluna supeior
        sup_col1, sup_col2, sup_col3, sup_col4 = st.columns(4)
        sup_col1.metric(label='Valor Máximo',value=f'{maximo}', border=True)
        sup_col2.metric(label='Valor Mínimo',value=f'{minimo}', border=True)
        sup_col3.metric(label='Soma', value=f'{soma}', border=True)
        sup_col4.metric(label='Média', value=f'{media:.2f}', border=True)

        # -- Coluna Inferior
        inf_col1, inf_col2, inf_col3, inf_col4 = st.columns(4)
        inf_col1.metric(label='Contagem de Valores',value=f'{contagem}', border=True)
        inf_col2.metric(label='Moda', value=f'{moda}', border=True)
        inf_col3.metric(label='Mediana', value=f'{mediana:.2f}', border=True)
        inf_col4.metric(label='Desvio Padrão',value=f'{desvio_padrao:.2f}', border=True)

    else:
        st.info('Nenhuma coluna categórica ou numérica disponível para gráfico.',
                icon=':material/warning:')



# ------ Visualização de múltiplas colunas numéricas ------
if upload is not None and len(colunas_numericas) > 1:
    st.divider()
    st.subheader('📊 Visualização de Múltiplas Colunas')
    st.markdown(
        '*Selecione **duas colunas numéricas** e o **tipo de gráfico** para fazer análises comparativas.*')
    
    # Criando colunas
    col1, col2 = st.columns(2)
    
    # Escolha da primeira coluna
    primeira_coluna = col1.selectbox(
        label='Escolha a primeira coluna:', options=colunas_numericas)


    # Garante que há pelo menos outra coluna para comparar
    outras_colunas = colunas_numericas.drop(primeira_coluna)
    if len(outras_colunas) == 0:
        st.info('Não há outra coluna numérica para comparar.')
    else:
        segunda_coluna = col2.selectbox(
            label='Escolha a segunda coluna:', options=outras_colunas)

        if primeira_coluna == segunda_coluna:
            st.warning('Selecione duas colunas diferentes!')
        else:
            escolha_grafico = st.selectbox(
                label='Selecione um tipo de gráfico:', options=['Nenhum', 'Barra', 'Linha', 'Área', 'Pizza', 'Dispersão', 'Caixa'])

            # --- Usuário seleciona a posição do gráfico
            opcoes2 = ['Vertical', 'Horizontal']
                
            posicao2 = st.pills('Escolha a posição do gráfico: ', options=opcoes2)


            # Função para gerar diferentes tipos de gráficos comparativos
            @st.cache_data
            def gerar_grafico(df, coluna_x, coluna_y, tipo, angulo):
                
                # -- Gráfico de barra + posicao do gráfico
                if tipo == 'Barra':
                    if posicao2 == 'Vertical':
                        angulo = 'v'
                    elif posicao2 == 'Horizontal':
                        angulo = 'h'
                    # Criação do gráfico de barra
                    fig = px.bar(df, x=coluna_x, y=coluna_y,
                                title=f'Gráfico de Barra: {coluna_x} X {coluna_y}', color=primeira_coluna,
                                orientation=angulo)
                    
                # -- Gráfico de linha   
                elif tipo == 'Linha':
                    fig = px.line(df, x=coluna_x, y=coluna_y,
                                  title=f'Gráfico de Linha: {coluna_x} X {coluna_y}')
                
                # -- Gráfico de Área + posicao do gráfico
                elif tipo == 'Área':
                    if posicao2 == 'Vertical':
                        angulo = 'v'
                    elif posicao2 == 'Horizontal':
                        angulo = 'h'
                    
                    # Criação do gráfico de área
                    fig = px.area(df, x=coluna_x, y=coluna_y,
                                  title=f'Gráfico de Área: {coluna_x} X {coluna_y}', color=primeira_coluna, orientation=angulo)
                
                # Gráfico de pizza
                elif tipo == 'Pizza':
                
                    fig = px.pie(
                        df, names=primeira_coluna, title=f"Gráfico de Pizza: Coluna - {primeira_coluna}.")

                    #Obs: O gráfioc de pizza do plotly só aceita 1 coluna
                    st.info(
                        'O gráfico de pizza não compara dados de 2 colunas! Altere as opções da 1ª coluna para visualizar os dados.', icon=':material/info:')
                    
                # Grafico de Dispersão
                elif tipo == 'Dispersão':
                    fig = px.scatter(
                        df, x=coluna_x, y=coluna_y, title=f"Gráfico de Dispersão: {coluna_x} X {coluna_y}", color=primeira_coluna)
                
                # Gráfio de caixa
                elif tipo == 'Caixa':
                    fig = px.box(df, x=coluna_x, y=coluna_y,
                                 title=f'Gráfico de Caixa: {coluna_x} X {coluna_y}')
                
                # Se não ouver escolha no gráfico, retornará None
                else:
                    fig = None
                return fig

            # Se o usuário escolher um tipo de gráfico, chamamos a função para criá-lo
            if escolha_grafico:
                fig = gerar_grafico(tabela, primeira_coluna,
                                    segunda_coluna, escolha_grafico, posicao2)
                if fig:
                    st.plotly_chart(fig)



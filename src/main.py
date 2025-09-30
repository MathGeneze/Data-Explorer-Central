import streamlit as st
import pandas as pd
import plotly.express as px

# ------- Layout da Página ---------#
# Opções de troca de temas da página.
# Usuário pode alternar entre Dark/ Light ou Gradient.
st.set_page_config(page_title="Tema Dinâmico", layout="wide")

# Se nenhum tema for selecionado, ele inicia com o Grandient
if "tema" not in st.session_state:
    st.session_state.tema = "gif"

label_map = {"dark": "🌙 Dark", "light": "☀️ Light", "gif": "🌎 Gradient"}

# Gera botões com as opções de temas
tema_escolhido = st.segmented_control(
    "Escolha o fundo:",
    options=list(label_map.values()),
    default=label_map[st.session_state.tema],
)

# Atualiza session_state
if tema_escolhido.startswith("🌙"):
    st.session_state.tema = "dark"
elif tema_escolhido.startswith("☀️"):
    st.session_state.tema = "light"
else:
    st.session_state.tema = "gif"

# Função para carregar CSS externo


def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Aplica o CSS do tema escolhido
if st.session_state.tema == "dark":
    load_css("styles/dark.css")
elif st.session_state.tema == "light":
    load_css("styles/light.css")
else:
    load_css("styles/gradient.css")


# ------ Cabeçalho da página ----- #
st.title('📚 Data Explorer Central')
st.subheader('Carregue seus dados. Explore estatísticas. Gere gráficos')
st.markdown('*Insira um **arquivo CSV** e explore as mais diversas estatísticas com **análise de gráficos**, **tabelas** e **métricas**.*')

# --- Upload de arquivo CSV ---
upload = st.file_uploader(
    label='Escolha um arquivo CSV:',
    type='csv'
)

# --- Função para ler o CSV com cache --- #
# O decorator @st.cache_data faz com que a função só execute novamente se o arquivo mudar, otimizando a performance da aplicação.


@st.cache_data
def carregar_csv(uploaded_file):
    """Lê o arquivo CSV enviado pelo usuário e retorna um DataFrame pandas."""
    return pd.read_csv(uploaded_file)


# --- Processamento do arquivo enviado --- #
if upload is not None:
    try:
        tabela = carregar_csv(upload)
        st.success('Arquivo carregado com sucesso!', icon=':material/check:')
    except Exception as error:
        st.error(
            f'Erro ao ler o seu arquivo: {error}. Verifique se é um arquivo CSV válido.', icon=':material/close:')


# ------ Exibição das primeiras linhas da tabela ------ #
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

    # --- Expansor contendo informações básicas sobre a tabela (tipo de dado, valores nulos e não nulos)
    with st.expander('Clique aqui para saber mais detalhes da tabela:', icon=':material/dataset:'):
        st.text('Informações descritivas sobre a tabela:')

        # Identifica colunas categóricas (texto) e numéricas
        colunas_categoricas = tabela.select_dtypes(exclude='number').columns
        colunas_numericas = tabela.select_dtypes(include='number').columns
        # Quantidade de colunas categóricas e numéricas
        qtd_colunas_categ = len(colunas_categoricas)
        qtd_colunas_num = len(colunas_numericas)

        st.write(f'• Colunas numéricas: {qtd_colunas_num}')
        st.write(f'• Colunas categóricas: {qtd_colunas_categ}')

        # Nova tabela contendo as informações detalhadas
        st.dataframe(
            pd.DataFrame({
                "Tipos de Dados": tabela.dtypes,
                "Valores Não Nulos": tabela.notnull().sum(),
                "Valores Nulos": tabela.isnull().sum()
            })
        )

    st.divider()

    # ------ Visualização de colunas únicas ------ #
    st.subheader('📈 Visualização de Colunas Únicas')
    st.markdown('*Escolha entre colunas **Numéricas** e **Categóricas (texto)**. Visualize em formato de **gráfico de barras** e **métricas**.*')

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
                opcoes = c1.pills(
                    'Escolha a posição do gráfico:', options=posicao)

                # --- Usuário pode selecionar a cor do gráfio
                escolha_cor = c2.color_picker(
                    "Escolha a cor do gráfico:", '#1585C1')

                if opcoes == 'Vertical':
                    # Exibe gráfico
                    st.bar_chart(tabela[coluna_unica].value_counts(
                    ), horizontal=False, color=escolha_cor)
                else:
                    st.bar_chart(tabela[coluna_unica].value_counts(
                    ), horizontal=True, color=escolha_cor)

        # --- Gráficos e métricas para coluna numérica ---
        if escolha == 'Numérica' and len(colunas_numericas) > 0:
            escolha_coluna_num = st.selectbox(
                'Selecione uma coluna numérica:', colunas_numericas)

            # --- Usuário seleciona a posição do gráfico
            posicao = ['Vertical', 'Horizontal']
            c1, c2 = st.columns(2)
            opcoes = c1.pills('Escolha a posição do gráfico:', options=posicao)

            # --- Usuário pode selecionar a cor do gráfio
            escolha_cor = c2.color_picker(
                "Escolha a cor do gráfico:", '#1585C1')

            if opcoes == 'Vertical':
                # Exibe gráfico
                st.bar_chart(tabela[escolha_coluna_num].value_counts(
                ), horizontal=False, color=escolha_cor)
            else:
                # Exibe gráfico de barras usando plotly para coluna numérica única
                contagem = tabela[escolha_coluna_num].value_counts(
                ).reset_index()
                contagem.columns = [escolha_coluna_num, 'Contagem']
                if opcoes == 'Vertical':
                    fig = px.bar(
                        contagem,
                        x=escolha_coluna_num,
                        y='Contagem',
                        color_discrete_sequence=[escolha_cor]
                    )
                else:
                    fig = px.bar(
                        contagem,
                        x='Contagem',
                        y=escolha_coluna_num,
                        orientation='h',
                        color_discrete_sequence=[escolha_cor]
                    )
                st.plotly_chart(fig, use_container_width=True)

        # Se o usuário não selecionar nenhuma opção, emite um alerta.
    else:
        st.warning('Nenhuma coluna selecionada.', icon=':material/warning:')

# Verifica se não há colunas categóricas nem numéricas e exibe uma mensagem informativa
if upload is not None and len(colunas_categoricas) == 0 and len(colunas_numericas) == 0:
    st.info('Nenhuma coluna categórica ou numérica disponível para gráfico.', icon=':material/warning:')


# ------ Métricas estatísticas ------ #
if upload is not None:
    st.divider()
    st.subheader('🌐 Métricas Estatísticas ')
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
    sup_col1.metric(label='Valor Máximo', value=f'{maximo}', border=True)
    sup_col2.metric(label='Valor Mínimo', value=f'{minimo}', border=True)
    sup_col3.metric(label='Soma', value=f'{soma}', border=True)
    sup_col4.metric(label='Média', value=f'{media:.2f}', border=True)

    # -- Coluna Inferior
    inf_col1, inf_col2, inf_col3, inf_col4 = st.columns(4)
    inf_col1.metric(label='Contagem de Valores',
                    value=f'{contagem}', border=True)
    inf_col2.metric(label='Moda', value=f'{moda}', border=True)
    inf_col3.metric(label='Mediana', value=f'{mediana:.2f}', border=True)
    inf_col4.metric(label='Desvio Padrão',
                    value=f'{desvio_padrao:.2f}', border=True)

    # Expansor contendo DataFrame com estatísticas descritivas
    expander = st.expander(
        'Clique aqui para saber mais informações estatísticas descritivas', icon=':material/info:')
    expander.dataframe(tabela.describe())


# ------ Visualização de múltiplas colunas numéricas ------
if upload is not None and (len(colunas_numericas) > 1 or len(colunas_categoricas) > 1):
    st.divider()
    st.subheader('📊 Visualização de Múltiplas Colunas')
    st.markdown(
        '*Selecione **duas colunas** e o **tipo de gráfico** para fazer análises comparativas.*')

    # Permite ao usuário escolher se quer comparar colunas numéricas ou categóricas
    tipo_comparacao = st.selectbox("Tipo de comparação:", ["Nenhuma", "Numérica", "Categórica"]
                                   )

    # ----- Colunas Numéricas ----- #
    # Se existir mais de uma coluna numérica, permite criar gráficos comparativos entre elas
    if tipo_comparacao == "Numérica" and len(colunas_numericas) > 1:
        col1, col2 = st.columns(2)

        # Usuário escolhe a primeira coluna numérica
        primeira_coluna = col1.selectbox(
            label='Escolha a primeira coluna:', options=colunas_numericas, key="num1")

        # Remove a primeira coluna da lista para evitar repetição
        outras_colunas = colunas_numericas.drop(primeira_coluna)

        if len(outras_colunas) == 0:
            st.info('Não há outra coluna numérica para comparar.')
        else:
            # Usuário escolhe a segunda coluna numérica
            segunda_coluna = col2.selectbox(
                label='Escolha a segunda coluna:', options=outras_colunas, key="num2")

            if primeira_coluna == segunda_coluna:
                st.warning('Selecione duas colunas diferentes!')
            else:
                # Usuário escolhe o tipo de gráfico desejado
                escolha_grafico = st.selectbox(label='Selecione um tipo de gráfico:', options=[
                                               'Barra', 'Linha', 'Área', 'Dispersão', 'Caixa'])

                # Usuário escolhe a orientação do gráfico
                opcoes2 = ['Vertical', 'Horizontal']
                posicao2 = st.pills(
                    'Escolha a posição do gráfico: ', options=opcoes2)

                # Função para gerar o gráfico de acordo com as escolhas do usuário
                def gerar_grafico_num(df, coluna_x, coluna_y, tipo, angulo):
                    if tipo == 'Barra':
                        orientation = 'v' if angulo == 'Vertical' else 'h'
                        fig = px.bar(df, x=coluna_x, y=coluna_y,
                                     orientation=orientation)
                    elif tipo == 'Linha':
                        fig = px.line(df, x=coluna_x, y=coluna_y)
                    elif tipo == 'Área':
                        orientation = 'v' if angulo == 'Vertical' else 'h'
                        fig = px.area(df, x=coluna_x, y=coluna_y)
                    elif tipo == 'Dispersão':
                        fig = px.scatter(df, x=coluna_x, y=coluna_y)
                    elif tipo == 'Caixa':
                        fig = px.box(df, x=coluna_x, y=coluna_y)
                    else:
                        fig = None
                    return fig

                # Gera e exibe o gráfico
                fig = gerar_grafico_num(
                    tabela, primeira_coluna, segunda_coluna, escolha_grafico, posicao2)
                if fig:
                    st.plotly_chart(fig)

    # ------- Colunas Categóricas ----- #
    # Se existir mais de uma coluna categórica, permite comparar categorias entre duas colunas
    elif tipo_comparacao == "Categórica" and len(colunas_categoricas) > 1:
        col1, col2 = st.columns(2)

        # Usuário escolhe a primeira coluna categórica
        primeira_coluna = col1.selectbox(
            label='Escolha a primeira coluna categórica:', options=colunas_categoricas, key="cat1")

        # Remove a primeira coluna da lista para evitar repetição
        outras_colunas = colunas_categoricas.drop(primeira_coluna)

        if len(outras_colunas) == 0:
            st.info('Não há outra coluna categórica para comparar.')
        else:
            # Usuário escolhe a segunda coluna categórica
            segunda_coluna = col2.selectbox(
                label='Escolha a segunda coluna categórica:', options=outras_colunas, key="cat2")

            if primeira_coluna == segunda_coluna:
                st.warning('Selecione duas colunas diferentes!')

            else:
                # Usuário escolhe o tipo de gráfico para comparação categórica
                escolha_grafico = st.selectbox(label='Selecione um tipo de gráfico:', options=[
                                               'Barra Agrupada', 'Mapa de Calor'])

                # Conta as combinações entre as duas colunas e plota gráfico de barras agrupadas
                if escolha_grafico == 'Barra Agrupada':
                    contagem = tabela.groupby(
                        [primeira_coluna, segunda_coluna]).size().reset_index(name='Contagem')
                    fig = px.bar(contagem, x=primeira_coluna, y='Contagem',
                                 color=segunda_coluna, barmode='group')
                    st.plotly_chart(fig)

                # Cria uma tabela cruzada (crosstab) e plota um Mapa de Calor
                elif escolha_grafico == 'Mapa de Calor':
                    heatmap_data = pd.crosstab(
                        tabela[primeira_coluna], tabela[segunda_coluna])
                    fig = px.imshow(heatmap_data, text_auto=True, aspect="auto", labels=dict(
                        x=segunda_coluna, y=primeira_coluna, color="Contagem"))
                    st.plotly_chart(fig)

    # Se o usuário não selecionar nenhuma opção, emite um alerta.
    elif tipo_comparacao == 'Nenhuma':
        st.warning('Nenhuma coluna selecionada.', icon=':material/warning:')

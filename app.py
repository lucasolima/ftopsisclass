import streamlit as st
import pandas as pd
import numpy as np
from matrizes.matriz_decisao import matriz_decisao, dados_matriz_decisao
from matrizes.matriz_perfil import matriz_perfil, dados_perfil
from pesos_criterios import pesos, tipo_criterios, pesos_
from variaveis_linguisticas import MB, B, M, A, MA, MBI, BI, IM, AI, MAI
from mapeamento.mapeamento import alternativas, criterios, importancia
from processamento.normalizar_matriz import normalizar_matriz
from processamento.ponderar_matriz import ponderar_matriz
from processamento.obter_solucao_ideal import obter_solucao_ideal
from processamento.calcular_distancia_euclidiana import calcular_distancia_euclidiana
from processamento.calcular_coeficiente_de_proximidade import calcular_coeficiente_de_proximidade
from processamento.gerar_matriz_coeficientes import gerar_matriz_coeficientes

st.set_page_config(page_title="FTOPSIS Class - Customizações de SIGS", layout="wide")

MAPA_SIGLAS = {
    "MB": MB, "B": B, "M": M, "A": A, "MA": MA,
    "MBI": MBI, "BI": BI, "IM": IM, "AI": AI, "MAI": MAI
}

def converter_para_sigla(val):
    if isinstance(val, (list, tuple, np.ndarray)):
        val_arr = np.array(val)
        for sigla, arr in MAPA_SIGLAS.items():
            if np.array_equal(val_arr, arr):
                return sigla
    return str(val)

def sigla_para_array(val):
    return MAPA_SIGLAS.get(val, val)

criterios_nomes = {k: v["criterio"] for k, v in criterios.items()}

def formatar_df_siglas(df):
    return df.applymap(converter_para_sigla) if hasattr(df, 'applymap') else df.apply(lambda col: col.map(converter_para_sigla))

def renomear_index_alternativas(df):
    if df is not None and not df.empty:
        novo_index = []
        for idx in df.index:
            if isinstance(idx, int):
                chave_alt = f"DC{idx + 1}"
            elif isinstance(idx, str) and idx.startswith("DC"):
                chave_alt = idx
            else:
                chave_alt = str(idx)
            
            novo_index.append(alternativas.get(chave_alt, str(idx)))
        df.index = novo_index
    return df

if "matriz_decisao_config" not in st.session_state:
    df_inicial = formatar_df_siglas(pd.DataFrame(dados_matriz_decisao))
    df_inicial = df_inicial.rename(columns=criterios_nomes)
    df_inicial = renomear_index_alternativas(df_inicial)
    for col in df_inicial.columns:
        df_inicial[col] = None
    st.session_state.matriz_decisao_config = df_inicial

if "pesos_config" not in st.session_state:
    df_pesos_inicial = formatar_df_siglas(pd.DataFrame(pesos_))
    df_pesos_inicial = df_pesos_inicial.rename(columns=criterios_nomes)
    for col in df_pesos_inicial.columns:
        df_pesos_inicial[col] = None
    st.session_state.pesos_config = df_pesos_inicial

if "matriz_perfil_config" not in st.session_state:
    df_perfil_inicial = formatar_df_siglas(pd.DataFrame(dados_perfil))
    df_perfil_inicial = df_perfil_inicial.rename(columns=criterios_nomes)
    df_perfil_inicial.index = ["Alta Prioridade", "Média Prioridade", "Baixa Prioridade"]
    st.session_state.matriz_perfil_config = df_perfil_inicial

@st.dialog("Editar Matriz de Perfis", width="large")
def modal_editar_perfis():
    st.markdown("Edite os valores base das classes de perfis:")
    df_editado = st.data_editor(st.session_state.matriz_perfil_config, use_container_width=True, height=(len(st.session_state.matriz_perfil_config) + 1) * 35 + 3, key="editor_modal_perfil")
    if st.button("Salvar alterações", type="primary"):
        st.session_state.matriz_perfil_config = df_editado
        st.rerun()

col_title, col_btn = st.columns([5, 1])
with col_title:
    st.subheader("FTOPSIS Class - Customizações de SIGS")
with col_btn:
    st.write("") # Margem para alinhar com o titulo
    if st.button("Editar Matriz de Perfis", use_container_width=True):
        modal_editar_perfis()

aba_config, aba_pesos, aba_entradas, aba_resultados = st.tabs(["Configuração do Modelo", "Configuração dos Pesos", "Entradas de Dados", "Resultados"])

with aba_config:
    st.markdown("**Formulário de Configuração das Demandas**")
    st.info("Preencha a avaliação das descrições dos critérios para cada demanda diretamente na estrutura abaixo.")
    
    lista_criterios_chaves = list(criterios.keys())
    nomes_criterios = [criterios[k]["criterio"] for k in lista_criterios_chaves]
    
    # Criar colunas: 1 para Demanda + N para Critérios
    cols = st.columns([2] + [1] * len(nomes_criterios))
    
    # Headers
    cols[0].markdown("**Demanda**")
    for i, crit_name in enumerate(nomes_criterios):
        cols[i+1].markdown(f"**{crit_name}**")
        
    lista_alts = list(st.session_state.matriz_decisao_config.index)
    
    for alt in lista_alts:
        cols = st.columns([2] + [1] * len(nomes_criterios))
        cols[0].markdown(f"*{alt}*")
        
        for i, k in enumerate(lista_criterios_chaves):
            v = criterios[k]
            col_nome = v["criterio"]
            opcoes_desc = [desc[0] for desc in v["descricao"]]
            mapa_sigla_desc = {desc[1]: desc[0] for desc in v["descricao"]}
            mapa_desc_sigla = {desc[0]: desc[1] for desc in v["descricao"]}
            
            sigla_atual = st.session_state.matriz_decisao_config.at[alt, col_nome]
            desc_atual = mapa_sigla_desc.get(sigla_atual, None)
            idx_default = opcoes_desc.index(desc_atual) if desc_atual in opcoes_desc else None
            
            with cols[i+1]:
                nova_desc = st.selectbox(
                    f"{alt}_{col_nome}",
                    options=opcoes_desc,
                    index=idx_default,
                    placeholder="Selecione...",
                    label_visibility="collapsed",
                    key=f"sel_{alt}_{k}"
                )
                st.session_state.matriz_decisao_config.at[alt, col_nome] = mapa_desc_sigla[nova_desc] if nova_desc else None
    
    df_decisao_siglas_from_config = st.session_state.matriz_decisao_config.copy()

with aba_pesos:
    st.markdown("**Configuração dos Pesos dos Critérios**")
    st.info("Atribua a importância para cada critério utilizado na classificação.")
    
    lista_criterios_chaves = list(criterios.keys())
    nomes_criterios = [criterios[k]["criterio"] for k in lista_criterios_chaves]
    
    cols = st.columns(len(nomes_criterios))
    for i, crit_name in enumerate(nomes_criterios):
        cols[i].markdown(f"**{crit_name}**")
        
    cols_pesos = st.columns(len(nomes_criterios))
    
    opcoes_peso_desc = list(importancia.values())
    mapa_sigla_peso = importancia
    mapa_peso_sigla = {desc: sigla for sigla, desc in importancia.items()}
    
    for i, k in enumerate(lista_criterios_chaves):
        v = criterios[k]
        col_nome = v["criterio"]
        
        sigla_peso_atual = st.session_state.pesos_config.at[0, col_nome]
        desc_peso_atual = mapa_sigla_peso.get(sigla_peso_atual, None)
        idx_peso_default = opcoes_peso_desc.index(desc_peso_atual) if desc_peso_atual in opcoes_peso_desc else None
        
        with cols_pesos[i]:
            novo_peso_desc = st.selectbox(
                f"peso_{col_nome}",
                options=opcoes_peso_desc,
                index=idx_peso_default,
                placeholder="Selecione...",
                label_visibility="collapsed",
                key=f"peso_sel_{k}"
            )
            st.session_state.pesos_config.at[0, col_nome] = mapa_peso_sigla[novo_peso_desc] if novo_peso_desc else None
    
    df_pesos_siglas_from_config = st.session_state.pesos_config.copy()

with aba_entradas:
    st.markdown("**Matriz de Decisão**", help="**Legenda:**  \n**MA** - Muito alto  \n**A** - Alto  \n**M** - Médio  \n**B** - Baixo  \n**MB** - Muito baixo")
    df_decisao_siglas = df_decisao_siglas_from_config.copy()
    df_decisao_editada = st.data_editor(df_decisao_siglas, use_container_width=True, height=(len(df_decisao_siglas) + 1) * 35 + 3, key="entrada_editor")

    st.markdown("**Matriz de Perfis**", help="**Legenda:**  \n**MA** - Muito alto  \n**A** - Alto  \n**M** - Médio  \n**B** - Baixo  \n**MB** - Muito baixo")
    df_perfil_siglas = st.session_state.matriz_perfil_config.copy()
    df_perfil_editada = st.data_editor(df_perfil_siglas, use_container_width=True, height=(len(df_perfil_siglas) + 1) * 35 + 3, key="perfil_editor")

    st.markdown("**Pesos dos Critérios**", help="**Legenda:**  \n**MBI** - Muito baixa importância  \n**BI** - Baixa importância  \n**IM** - Importância média  \n**AI** - Alta importância  \n**MAI** - Muito alta importância")
    df_pesos_siglas = df_pesos_siglas_from_config.copy()
    df_pesos_editada = st.data_editor(df_pesos_siglas, use_container_width=True, height=(len(df_pesos_siglas) + 1) * 35 + 3, key="pesos_editor")

# ----------------- RECALCULAR TOPSIS -----------------

inv_criterios = {v["criterio"]: k for k, v in criterios.items()}

if df_decisao_editada.isnull().values.any() or df_pesos_editada.isnull().values.any():
    st.warning("O modelo não possui todos os dados preenchidos. Por favor, acesse a aba 'Configuração do Modelo' e preencha todos os critérios e pesos de todas as alternativas para gerar os resultados do TOPSIS.")
    st.stop()

# 1. Recuperar e converter de volta as matrizes editadas pra arrays fuzzy
dec_revertida = df_decisao_editada.rename(columns=inv_criterios).reset_index(drop=True)
matriz_decisao_calc = dec_revertida.applymap(sigla_para_array) if hasattr(dec_revertida, 'applymap') else dec_revertida.map(sigla_para_array)

perf_revertida = df_perfil_editada.rename(columns=inv_criterios).reset_index(drop=True)
matriz_perfil_calc = perf_revertida.applymap(sigla_para_array) if hasattr(perf_revertida, 'applymap') else perf_revertida.map(sigla_para_array)

pesos_revertida = df_pesos_editada.rename(columns=inv_criterios).reset_index(drop=True)
pesos_calc = pesos_revertida.applymap(sigla_para_array) if hasattr(pesos_revertida, 'applymap') else pesos_revertida.map(sigla_para_array)

# 2. Processamento
matriz_decisao_normalizada = normalizar_matriz(matriz_decisao_calc, tipo_criterios)
matriz_decisao_ponderada = ponderar_matriz(matriz_decisao_normalizada, pesos_calc)

matriz_perfil_normalizada = normalizar_matriz(matriz_perfil_calc, tipo_criterios, matriz_referencia=matriz_decisao_calc)
matriz_perfil_ponderada = ponderar_matriz(matriz_perfil_normalizada, pesos_calc)

alta_prioridade, media_prioridade, baixa_prioridade = obter_solucao_ideal(matriz_perfil_ponderada)

d_mais_alta_prioridade, d_menos_alta_prioridade = calcular_distancia_euclidiana(matriz_decisao_ponderada, alta_prioridade)
d_mais_media_prioridade, d_menos_media_prioridade = calcular_distancia_euclidiana(matriz_decisao_ponderada, media_prioridade)
d_mais_baixa_prioridade, d_menos_baixa_prioridade = calcular_distancia_euclidiana(matriz_decisao_ponderada, baixa_prioridade)

cc_alta_prioridade = calcular_coeficiente_de_proximidade(d_mais_alta_prioridade, d_menos_alta_prioridade)
cc_media_prioridade = calcular_coeficiente_de_proximidade(d_mais_media_prioridade, d_menos_media_prioridade)
cc_baixa_prioridade = calcular_coeficiente_de_proximidade(d_mais_baixa_prioridade, d_menos_baixa_prioridade)

dict_ccs = {
    'Alta Prioridade': cc_alta_prioridade,
    'Média Prioridade': cc_media_prioridade,
    'Baixa Prioridade': cc_baixa_prioridade
}

matriz_coeficientes = gerar_matriz_coeficientes(dict_ccs)

# Exibição básica no terminal
print("\n--- Matriz de Coeficientes de Proximidade (CC) ---")
print(matriz_coeficientes)

with aba_resultados:
    matriz_coeficientes = matriz_coeficientes.round(3)
    matriz_coeficientes = renomear_index_alternativas(matriz_coeficientes)

    st.subheader("Matriz de Coeficientes de Proximidade")
    st.dataframe(matriz_coeficientes.style.format("{:.3f}"), use_container_width=True, height=(len(matriz_coeficientes) + 1) * 35 + 3)

    st.subheader("Ranking - Alta Prioridade")
    matriz_rankeada = matriz_coeficientes[['Alta Prioridade']].sort_values(by="Alta Prioridade", ascending=False)
    st.dataframe(matriz_rankeada.style.format("{:.3f}"), use_container_width=True, height=(len(matriz_rankeada) + 1) * 35 + 3)

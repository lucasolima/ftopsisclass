import streamlit as st
import pandas as pd
import numpy as np
from matrizes.matriz_decisao import matriz_decisao, dados_matriz_decisao
from matrizes.matriz_perfil import matriz_perfil, dados_perfil
from pesos_criterios import pesos, tipo_criterios, pesos_
from variaveis_linguisticas import MB, B, M, A, MA, MBI, BI, IM, AI, MAI
from mapeamento.mapeamento import alternativas, criterios
from processamento.normalizar_matriz import normalizar_matriz
from processamento.ponderar_matriz import ponderar_matriz
from processamento.obter_solucao_ideal import obter_solucao_ideal
from processamento.calcular_distancia_euclidiana import calcular_distancia_euclidiana
from processamento.calcular_coeficiente_de_proximidade import calcular_coeficiente_de_proximidade
from processamento.gerar_matriz_coeficientes import gerar_matriz_coeficientes

st.set_page_config(page_title="Sistema Fuzzy TOPSIS", layout="wide")
st.subheader("Sistema Fuzzy TOPSIS")

aba_entradas, aba_resultados = st.tabs(["Entradas de Dados", "Resultados"])

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

with aba_entradas:
    st.markdown("**Matriz de Decisão**", help="**Legenda:**  \n**MA** - Muito alto  \n**A** - Alto  \n**M** - Médio  \n**B** - Baixo  \n**MB** - Muito baixo")
    df_decisao_siglas = formatar_df_siglas(pd.DataFrame(dados_matriz_decisao))
    df_decisao_siglas = df_decisao_siglas.rename(columns=criterios)
    df_decisao_siglas = renomear_index_alternativas(df_decisao_siglas)
    df_decisao_editada = st.data_editor(df_decisao_siglas, use_container_width=True, height=(len(df_decisao_siglas) + 1) * 35 + 3)

    st.markdown("**Matriz de Perfis**", help="**Legenda:**  \n**MA** - Muito alto  \n**A** - Alto  \n**M** - Médio  \n**B** - Baixo  \n**MB** - Muito baixo")
    df_perfil_siglas = formatar_df_siglas(pd.DataFrame(dados_perfil))
    df_perfil_siglas = df_perfil_siglas.rename(columns=criterios)
    df_perfil_siglas.index = ["Alta Prioridade", "Média Prioridade", "Baixa Prioridade"]
    df_perfil_editada = st.data_editor(df_perfil_siglas, use_container_width=True, height=(len(df_perfil_siglas) + 1) * 35 + 3)

    st.markdown("**Pesos dos Critérios**", help="**Legenda:**  \n**MBI** - Muito baixa importância  \n**BI** - Baixa importância  \n**IM** - Importância média  \n**AI** - Alta importância  \n**MAI** - Muito alta importância")
    df_pesos_siglas = formatar_df_siglas(pd.DataFrame(pesos_))
    df_pesos_siglas = df_pesos_siglas.rename(columns=criterios)
    df_pesos_editada = st.data_editor(df_pesos_siglas, use_container_width=True, height=(len(df_pesos_siglas) + 1) * 35 + 3)

# ----------------- RECALCULAR TOPSIS -----------------

inv_criterios = {v: k for k, v in criterios.items()}

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

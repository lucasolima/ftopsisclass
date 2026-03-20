import pandas as pd
import numpy as np

def calcular_distancia_euclidiana(matriz, solucao_ideal):
    """
    Calcula as distâncias D+ e D- a partir da matriz de decisão (ponderada) 
    e as soluções ideais (positiva na linha 0, negativa na linha 1).
    Retorna dois DataFrames (d_mais e d_menos) contendo os valores para 
    cada critério e a coluna final com o somatório dessas distâncias.
    """
    d_mais = pd.DataFrame(index=matriz.index, columns=matriz.columns)
    d_menos = pd.DataFrame(index=matriz.index, columns=matriz.columns)

    for coluna in matriz.columns:
        p_ideal = solucao_ideal[coluna].iloc[0]
        n_ideal = solucao_ideal[coluna].iloc[1]

        # Distância fuzzy euclidiana D+
        d_mais[coluna] = matriz[coluna].apply(
            lambda x: np.sqrt(sum((x[i] - p_ideal[i]) ** 2 for i in range(3)) / 3.0)
        )
        # Distância fuzzy euclidiana D-
        d_menos[coluna] = matriz[coluna].apply(
            lambda x: np.sqrt(sum((x[i] - n_ideal[i]) ** 2 for i in range(3)) / 3.0)
        )

    # Adicionar somatório total em uma nova coluna
    d_mais['D+'] = d_mais.sum(axis=1)
    d_menos['D-'] = d_menos.sum(axis=1)

    return d_mais, d_menos
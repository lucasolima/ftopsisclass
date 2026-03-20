import numpy as np

def ponderar_matriz(matriz_normalizada, pesos):
    matriz_ponderada = matriz_normalizada.copy(deep=True)

    for coluna in matriz_normalizada.columns:
        peso_coluna = pesos[coluna].iloc[0]
        matriz_ponderada[coluna] = matriz_normalizada[coluna].apply(
            lambda x: x * peso_coluna
        )

    return matriz_ponderada
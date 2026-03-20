import pandas as pd

def obter_solucao_ideal(matriz_ponderada):
    """
    Retorna três matrizes representando os pares de solução ideal 
    (Positiva e Negativa) baseando-se nos perfis das classes:
    
    matriz_1: Perfil 1 (linha 0) e Perfil 3 (linha 2)
    matriz_2: Perfil 2 (linha 1) e Perfil 3 (linha 2)
    matriz_3: Perfil 3 (linha 2) e Perfil 1 (linha 0)
    """
    matriz_1 = matriz_ponderada.iloc[[0, 2]].copy().reset_index(drop=True)
    matriz_2 = matriz_ponderada.iloc[[1, 2]].copy().reset_index(drop=True)
    matriz_3 = matriz_ponderada.iloc[[2, 0]].copy().reset_index(drop=True)
    
    return matriz_1, matriz_2, matriz_3
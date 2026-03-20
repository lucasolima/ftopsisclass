import numpy as np

def normalizar_matriz(matriz_decisao, tipo_criterios):
    matriz_normalizada = matriz_decisao.copy(deep=True)

    for coluna in matriz_decisao.columns:
        valores_coluna = np.vstack(matriz_decisao[coluna].to_numpy())
        criterio = tipo_criterios.get(coluna, "beneficio")

        if criterio == "beneficio":
            maior_ultima_coluna = np.max(valores_coluna[:, 2])
            if maior_ultima_coluna == 0:
                maior_ultima_coluna = 1.0
            matriz_normalizada[coluna] = matriz_decisao[coluna].apply(
                lambda x: np.floor((x / maior_ultima_coluna) * 10 + 0.5) / 10
            )
        elif criterio == "custo":
            menor_primeira_coluna = np.min(valores_coluna[:, 0])
            matriz_normalizada[coluna] = matriz_decisao[coluna].apply(
                lambda x: np.floor(
                    np.divide(menor_primeira_coluna, x[::-1], out=np.zeros_like(x, dtype=float), where=x[::-1] != 0) * 10 + 0.5
                ) / 10
            )
        else:
            raise ValueError(f"Tipo de critério inválido para {coluna}: {criterio}")

    return matriz_normalizada



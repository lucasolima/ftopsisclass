import pandas as pd

def calcular_coeficiente_de_proximidade(d_mais, d_menos):
    """
    Calcula o coeficiente de proximidade (C) a partir das distâncias D+ e D-.
    C é calculado como C = D- / (D+ + D-), onde D+ é a distância para a solução ideal positiva
    e D- é a distância para a solução ideal negativa.
    Retorna um DataFrame contendo o coeficiente de proximidade para cada alternativa.
    """
    coeficiente_proximidade = pd.DataFrame(index=d_mais.index, columns=['C'])
    
    for indice in d_mais.index:
        d_plus = d_mais.loc[indice, 'D+']
        d_minus = d_menos.loc[indice, 'D-']
        if (d_plus + d_minus) != 0:
            coeficiente_proximidade.loc[indice, 'C'] = d_minus / (d_plus + d_minus)
        else:
            coeficiente_proximidade.loc[indice, 'C'] = 0.0  # Evitar divisão por zero

    return coeficiente_proximidade
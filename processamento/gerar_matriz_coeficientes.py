import pandas as pd

def gerar_matriz_coeficientes(dict_cc):
    """
    Recebe um dicionário onde a chave é o nome da prioridade 
    e o valor é o DataFrame de coeficientes (C).
    Combina lado a lado em uma matriz onde cabecalho é o tipo da prioridade
    e as linhas são DC1, DC2, ...
    """
    df_result = pd.DataFrame()
    
    for nome_prioridade, df_cc in dict_cc.items():
        # df_cc['C'] tem as proximidades
        df_result[nome_prioridade] = df_cc['C']
    
    # Renomeando as linhas
    df_result.index = [f"DC{i+1}" for i in range(len(df_result))]
    
    return df_result

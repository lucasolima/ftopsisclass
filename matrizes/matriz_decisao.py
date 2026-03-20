import pandas as pd
from variaveis_linguisticas import MB, B, M, A, MA

dados_matriz_decisao = {
    "C1": [A, M, M, M, M, M, M, A, M],      # Alinhamento estratégico PEI, PDI, PDTIC, EGD
    "C2": [MB, B, MB, A, MB, B, A, MB, MA], # Exigência legal / regulatória
    "C3": [A, B, A, M, A, M, A, MA, M],     # Abrangência / impacto na comunidade da UFPE
    "C4": [MB, B, MB, MB, MB, MB, B, A, A], # Complexidade
    "C5": [M, M, B, A, B, B, B, A, A],      # Esforço
    "C6": [B, A, B, M, B, A, B, M, A],      # Tempo total
}

matriz_decisao = pd.DataFrame(dados_matriz_decisao)

# print(matriz_decisao)
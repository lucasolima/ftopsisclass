import pandas as pd
from variaveis_linguisticas import MB, B, M, A, MA

dados_perfil = {
    'C1': [A, M, B],
    'C2': [A, M, MB],
    'C3': [A, M, B],
    'C4': [B, M, MA],
    'C5': [B, M, MA],
    'C6': [MB, M, MA],
}

matriz_perfil = pd.DataFrame(dados_perfil)

mapeamento_perfil = {0: 'Alta Prioridade', 1: 'Média Prioridade', 2: 'Baixa Prioridade'}

#print(matriz_perfil)
import numpy as np

# Váriáveis Linguísticas para avaliação alternativas
MB = np.array([1.0, 1.0, 2.0]) # Muito baixo
B = np.array([1.0, 2.0, 3.0])  # Baixo
M = np.array([2.0, 3.0, 4.0])  # Medio
A = np.array([3.0, 4.0, 5.0])  # Alto
MA = np.array([4.0, 5.0, 6.0]) # Muito alto

#Variáveis Linguísticas dos pesos dos critérios
MBI = np.array([0.1, 0.1, 0.2]) # Muito baixa importância
BI = np.array([0.1, 0.2, 0.3])  # Baixa importância
IM = np.array([0.2, 0.3, 0.4])  # Importância média
AI = np.array([0.3, 0.4, 0.5])  # Alta importância
MAI = np.array([0.4, 0.5, 0.6]) # Muito alta importância
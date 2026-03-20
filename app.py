from matrizes.matriz_decisao import matriz_decisao
from matrizes.matriz_perfil import matriz_perfil
from processamento.normalizar_matriz import normalizar_matriz
from processamento.ponderar_matriz import ponderar_matriz
from pesos_criterios import pesos, tipo_criterios

matriz_decisao_normalizada = normalizar_matriz(matriz_decisao, tipo_criterios)
matriz_decisao_ponderada = ponderar_matriz(matriz_decisao_normalizada, pesos)

matriz_perfil_normalizada = normalizar_matriz(matriz_perfil, tipo_criterios, matriz_referencia=matriz_decisao)
matriz_perfil_ponderada = ponderar_matriz(matriz_perfil_normalizada, pesos)

print(matriz_decisao_ponderada)
print(matriz_perfil_ponderada)

from processamento.obter_solucao_ideal import obter_solucao_ideal

m1, m2, m3 = obter_solucao_ideal(matriz_perfil_ponderada)

print("Solução Ideal Classe 1:\n", m1, "\n")
print("Solução Ideal Classe 2:\n", m2, "\n")
print("Solução Ideal Classe 3:\n", m3, "\n")

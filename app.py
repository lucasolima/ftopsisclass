from matriz_decisao import matriz_decisao
from matriz_perfil import matriz_perfil, mapeamento_perfil
from processamento.normalizar_matriz import normalizar_matriz
from processamento.ponderar_matriz import ponderar_matriz
from pesos_criterios import pesos, tipo_criterios

matriz_decisao_normalizada = normalizar_matriz(matriz_decisao, tipo_criterios)
matriz_decisao_ponderada = ponderar_matriz(matriz_decisao_normalizada, pesos)

matriz_perfil_normalizada = normalizar_matriz(matriz_perfil, tipo_criterios, matriz_referencia=matriz_decisao)
matriz_perfil_ponderada = ponderar_matriz(matriz_perfil_normalizada, pesos)

print(matriz_decisao_ponderada)
print(matriz_perfil_ponderada)
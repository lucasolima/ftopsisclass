from matrizes.matriz_decisao import matriz_decisao
from matrizes.matriz_perfil import matriz_perfil
from pesos_criterios import pesos, tipo_criterios
from processamento.normalizar_matriz import normalizar_matriz
from processamento.ponderar_matriz import ponderar_matriz
from processamento.obter_solucao_ideal import obter_solucao_ideal
from processamento.calcular_distancia_euclidiana import calcular_distancia_euclidiana
from processamento.calcular_coeficiente_de_proximidade import calcular_coeficiente_de_proximidade
from processamento.gerar_matriz_coeficientes import gerar_matriz_coeficientes


matriz_decisao_normalizada = normalizar_matriz(matriz_decisao, tipo_criterios)
matriz_decisao_ponderada = ponderar_matriz(matriz_decisao_normalizada, pesos)
matriz_perfil_normalizada = normalizar_matriz(matriz_perfil, tipo_criterios, matriz_referencia=matriz_decisao)
matriz_perfil_ponderada = ponderar_matriz(matriz_perfil_normalizada, pesos)

#print(matriz_perfil_normalizada["C5"])
#print(matriz_perfil_ponderada["C5"])

alta_prioridade, media_prioridade, baixa_prioridade = obter_solucao_ideal(matriz_perfil_ponderada)

d_mais_alta_prioridade, d_menos_alta_prioridade = calcular_distancia_euclidiana(matriz_decisao_ponderada, alta_prioridade)
d_mais_media_prioridade, d_menos_media_prioridade = calcular_distancia_euclidiana(matriz_decisao_ponderada, media_prioridade)
d_mais_baixa_prioridade, d_menos_baixa_prioridade = calcular_distancia_euclidiana(matriz_decisao_ponderada, baixa_prioridade)

#print(d_mais_alta_prioridade.round(3))
#print(d_menos_alta_prioridade.round(3))


cc_alta_prioridade = calcular_coeficiente_de_proximidade(d_mais_alta_prioridade, d_menos_alta_prioridade)
cc_media_prioridade = calcular_coeficiente_de_proximidade(d_mais_media_prioridade, d_menos_media_prioridade)
cc_baixa_prioridade = calcular_coeficiente_de_proximidade(d_mais_baixa_prioridade, d_menos_baixa_prioridade)

dict_ccs = {
    'Alta Prioridade': cc_alta_prioridade,
    'Média Prioridade': cc_media_prioridade,
    'Baixa Prioridade': cc_baixa_prioridade
}
matriz_coeficientes = gerar_matriz_coeficientes(dict_ccs)

print("\n--- Matriz de Coeficientes de Proximidade (CC) ---")
print(matriz_coeficientes.astype(float).round(3))
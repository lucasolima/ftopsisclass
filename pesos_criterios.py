from variaveis_linguisticas import AI, MAI, IM, BI
import pandas as pd

tipo_criterios = {
    "C1": "beneficio",
    "C2": "beneficio",
    "C3": "beneficio",
    "C4": "custo",
    "C5": "custo",
    "C6": "custo"
}

pesos_ = {
    "C1": [AI],
    "C2": [MAI],
    "C3": [IM],
    "C4": [BI],
    "C5": [BI],
    "C6": [BI]
}

pesos = pd.DataFrame(pesos_)

#print(pesos)
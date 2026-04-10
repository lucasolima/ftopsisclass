alternativas = {
    "DC1": "SIPAC - Autenticação pelo gov.br",
    "DC2": "SIPAC - Migração dos módulos de patrimômio e inventário para o SIADS",
    "DC3": "SIPAC - Implantação do módulo de bolsas",
    "DC4": "SIGRH - Aprimoramento PID/RID - Progressão docente",
    "DC5": "SIGAA - Implantação do módulo de pesquisas",
    "DC6": "SIGAA - Implantação do módulo de assistência estudantil",
    "DC7": "SIGAA - Central de estágios",
    "DC8": "Processos seletivos",
    "DC9": "Emissão, guarda e integração do serviço de diploma digital com a RNP"
}

criterios = {
    "C1": {
            "criterio": "Alinhamento estratégico a planos institucionais",
                "descricao": [
                    ["Prioridade explícita da alta gestão", "MA", "MAI"],
                    ["Alinhado a estratégias governamentais", "A", "AI"],
                    ["Previsto em PDTIC anterior", "M", "IM"],
                    ["Previsto em planos estratégicos", "B", "BI"],
                    ["Não está previsto em nenhum plano", "MB", "MBI"]
                ]
        },
        
    "C2": {
            "criterio": "Exigência legal/regulatória",
                "descricao": [
                    ["Mais de uma exigência legal/regulatória externa", "MA", "MAI"],
                    ["Mais de uma exigência legal/regulatória interna", "A", "AI"],
                    ["Uma exigência legal/regulatória externa", "M", "IM"],
                    ["Uma exigência legal/regulatória interna", "B", "BI"],
                    ["Não é uma exigência legal/regulatória", "MB", "MBI"]
                ]
        },
    "C3": {
            "criterio": "Abrangência na comunidade universitária",
                "descricao": [
                    ["Universidade e a sociedade", "MA", "MAI"],
                    ["Maioria ou toda a comunidade acadêmica", "A", "AI"],
                    ["Maioria dos técnicos-administrativos e/ou a maioria dos discentes e/ou docentes", "M", "IM"],
                    ["Centros, órgãos suplementares ou pró-reitorias isoladamente", "B", "BI"],
                    ["Afeta apenas um departamento ou setor", "MB", "MBI"]
                ]
        },
    "C4": {
            "criterio": "Complexidade",
                "descricao": [
                    ["Altíssima (requisitos extremamente complexos e ambíguos, alta interdependência entre sistemas, muitas partes interessadas com necessidades conflitantes, alto risco de mudanças)", "MA", "MBI"],
                    ["Alta (requisitos complexos e ambíguos, significativa interdependência entre sistemas, muitas partes interessadas, risco moderado a alto de mudanças)", "A", "BI"],
                    ["Média (Requisitos moderadamente complexos e claros, interdependência entre sistemas, algumas partes interessadas, risco moderado de mudanças)", "M", "IM"],
                    ["Baixa (Requisitos relativamente claros e precisos, interdependência limitada entre sistemas, algumas partes interessadas, baixo risco de mudanças)", "B", "AI"],
                    ["Baixíssima (Requisitos claramente definidos e precisos, mínima interdependência entre sistemas, poucas partes interessadas, muito baixo risco de mudanças)", "MB", "MAI"]
                ]
        },
    "C5": {
            "criterio": "Esforço",
                "descricao": [
                    ["Altíssimo (customização e integração de alta complexidade, envolvendo mais de um setor e dois ou mais desenvolvedores, com interdependências significativas e coordenação necessária entre equipes)", "MA", "MBI"],
                    ["Alto (customização que envolve dois ou mais desenvolvedores, tarefas de complexidade média a alta, requerendo coordenação entre desenvolvedores e possivelmente algumas outras áreas)", "A", "BI"],
                    ["Médio (customização que pode envolver um ou mais desenvolvedores, tarefas de complexidade média e algumas interdependências)", "M", "IM"],
                    ["Baixo (customização pontual, envolvendo um desenvolvedor, tarefas claramente definidas e de baixa complexidade)", "B", "AI"],
                    ["Baixíssimo (tarefas simples que envolvem um único desenvolvedor por um curto período)", "MB", "MAI"]
                ]
        },
    "C6": {
            "criterio": "Tempo Total",
                "descricao": [
                    ["Mais de um ano", "MA", "MBI"],
                    ["De 6 meses a um ano", "A", "BI"],
                    ["De 3 a 6 meses", "M", "IM"],
                    ["De 1 a 3 meses", "B", "AI"],
                    ["Até 1 mês", "MB", "MAI"]
                ]
        },
}

importancia = {
    "MBI": "Muito baixa importância",
    "BI": "Baixa importância",
    "IM": "Importância média",
    "AI": "Alta importância",
    "MAI": "Muito alta importância"
}
def cabecalho_tabela(nome_arquivo, layout):
    
    layout = layout.replace("_v1", "").replace("_v2", "").replace("_v3", "")
    
    dados = {
        "arquivo": nome_arquivo,
        "instituicao": layout,
        "vencimento": "",
        "data_documento": "",
        "data_processamento": "",
        "numero_documento": "",
        "nosso_numero": "",
        "valor_documento": "",
        "beneficiario": "",
        "cnpj_beneficiario": "",
        "pagador": "",
        "cnpj_pagador": "",
        "linha_digitavel": "",
        "tipo_operacao": ""
    }
    return dados 
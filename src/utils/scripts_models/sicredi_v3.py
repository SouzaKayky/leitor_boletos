from utils.regex import buscar_regex
from utils.normalizar_cnpj import normalizar_cnpj_areal
import re 

def extrair_boleto_sicredi_v3(texto, nome_arquivo=""):
    dados = {
        "arquivo": nome_arquivo,
        "instituicao": "Sicredi",
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

    linhas = texto.splitlines()
    total_linhas = len(linhas)

    for i, linha in enumerate(linhas):
        linha = linha.strip()
        
        if "Vencimento" in linha and i + 1 < total_linhas:
            dados["vencimento"] = buscar_regex(r'(\d{2}/\d{2}/\d{4})', linhas[i+1])
        
        if "Data do Documento" in linha and i + 1 < total_linhas:
            dados["data_documento"] = buscar_regex(r'(\d{2}/\d{2}/\d{4})', linhas[i+1])

        if "Data do Processamento" in linha and i + 1 < total_linhas:
            dados["data_processamento"] = buscar_regex(r'(\d{2}/\d{2}/\d{4})', linhas[i+1])

        if re.search(r'\d{2}/\d{2}/\d{4}.*', linha):
            dados["numero_documento"] = buscar_regex(r'\d{2}/\d{2}/\d{4}\s+([0-9\-]+)', linha)
            dados["nosso_numero"] = buscar_regex(r'(25/\d{6}-\d)', linha)

        if "Valor do Documento" in linha or "Valor Moeda" in linha and i + 1 < total_linhas:
            dados["valor_documento"] = buscar_regex(r'R?\$?\s*([\d\.,]+)', linhas[i+1])

        if "Beneficiário Agência" in linha and i + 1 < total_linhas:
            dados["beneficiario"] = buscar_regex(r'^([A-Z\s]+)', linhas[i+1])
            
        if "Beneficiário:" in linha and i + 1 < total_linhas:
            dados["cnpj_beneficiario"] = buscar_regex(r'(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})|24826317000140', linha)

        if "Pagador" in linha and i + 1 < total_linhas:
            linha_pagador = linhas[i+1]
            dados["pagador"] = buscar_regex(r'^([A-Z\s]+)', linha_pagador)
            dados["cnpj_pagador"] = buscar_regex(r'(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})|24826317000140', linha_pagador)

        if "748-X" in linha and len(linha) > 40:
            dados["linha_digitavel"] = buscar_regex(r'(748[\d\. ]+)', linha)

    cnpj_chave = "24826317000140"
    if normalizar_cnpj_areal(dados["cnpj_beneficiario"]) == cnpj_chave: 
        dados["tipo_operacao"] = "boleto de cobrança"
    elif normalizar_cnpj_areal(dados["cnpj_pagador"]) == cnpj_chave:
        dados["tipo_operacao"] = "pagamento de serviço/produto"
    else:
        dados["tipo_operacao"] = "outro"

    return dados

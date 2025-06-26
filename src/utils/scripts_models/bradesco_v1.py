from utils.regex import buscar_regex
from utils.normalizar_cnpj import normalizar_cnpj_areal
from utils.identificar_modelo_layout import identificar_layout
from utils.cabecalho_tabela import cabecalho_tabela

def extrair_boleto_bradesco_v1(texto, dados):

    linhas = texto.splitlines()
    total_linhas = len(linhas)

    for i, linha in enumerate(linhas):
        linha = linha.strip()

        if "Vencimento" in linha and i + 1 < total_linhas:
            dados["vencimento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', linhas[i+1])
        
        if "Data do Documento" in linha and i + 1 < total_linhas:
            dados["data_documento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', linhas[i+1])

        if "Data de Processamento" in linha and i + 1 < total_linhas:
            dados["data_processamento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', linhas[i+1])

        if "Nr. do Documento" in linha and i + 1 < total_linhas:
            dados["numero_documento"] = buscar_regex(
                r'\d{2}/\d{2}/\d{4}\s+([0-9\-]+)', linhas[i+1])
            
        if "Nosso Número" in linha and i + 1 < total_linhas:
            dados["nosso_numero"] = buscar_regex(
                r'(\d{2}/\d{11}-\d|\d{2}/\d{11}-\d)', linhas[i+1])

        if "Valor do Documento" in linha and i + 1 < total_linhas:
            dados["valor_documento"] = buscar_regex(
                r'R\$?\s*([\d\.,]+)', linhas[i+1])

        if "Beneficiário Final/CNPJ/Endereço:" in linha and i + 1 < total_linhas:
            dados["beneficiario"] = buscar_regex(
                r'^(.*?)\s+CNPJ:', linhas[i+1])
            dados["cnpj_beneficiario"] = buscar_regex(
                r':\s*(\d{1,2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}|\d{13,14})', linhas[i+1])

        if "Pagador/CNPJ/Endereço" in linha and i + 1 < total_linhas:
            dados["pagador"] = buscar_regex(
                r'^(.*?)\s+CNPJ:', linhas[i+1])
            dados["cnpj_pagador"] = buscar_regex(
                r':\s*(\d{1,2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}|\d{13,14})', linhas[i+1])

        if "237-2" in linha and len(linha) > 40:
            dados["linha_digitavel"] = buscar_regex(
                r'(237[\d])', linha)

    cnpj_chave = "24826317000140"
    if normalizar_cnpj_areal(
        dados["cnpj_beneficiario"]) == cnpj_chave:
        dados["tipo_operacao"] = "boleto de cobrança"
    elif normalizar_cnpj_areal(
        dados["cnpj_pagador"]) == cnpj_chave:
        dados["tipo_operacao"] = "pagamento de serviço/produto"
    else:
        dados["tipo_operacao"] = "outro"

    return dados
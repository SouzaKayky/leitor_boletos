from utils.regex import buscar_regex
from utils.normalizar_cnpj import normalizar_cnpj_areal
import re 

def extrair_receita_federal_v1(texto, dados):

    linhas = texto.splitlines()
    total_linhas = len(linhas)    
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()

        if i + 1 < total_linhas:
            pega_linha_abaixo = linhas[i + 1].strip()
            
        else:
            pega_linha_abaixo = ""
        if "Período de Apuração Data de Vencimento Número do Documento" in linha and i + 1 < total_linhas:
            dados["vencimento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', pega_linha_abaixo)
            dados["data_documento"] = buscar_regex(
                r'(\b[A-ZÁ-Úa-zá-ú]{3,9}/\d{4}\b)', pega_linha_abaixo)
            dados["data_processamento"] = buscar_regex(
                r'(\b[A-ZÁ-Úa-zá-ú]{3,9}/\d{4}\b)', pega_linha_abaixo)
            dados["numero_documento"] = buscar_regex(
                r'(\d{2}\.\d{2}\.\d{5}\.\d{7}-\d)', pega_linha_abaixo)

        if "Nº Recibo Declaração:" in linha and i + 1 < total_linhas:
            dados["nosso_numero"] = buscar_regex(
                r'(\d{14})', linha)

        if "Valor Total do Documento" in linha and i + 1 < total_linhas:
            dados["valor_documento"] = buscar_regex(
                r'R?\$?\s*([\d\.,]+)', pega_linha_abaixo)
       
        if "Beneficiário Final/CNPJ/Endereço:" in linha and i + 1 < total_linhas:
            dados["beneficiario"] = buscar_regex(
                r'^(.*?)\s+CNPJ:', pega_linha_abaixo)
            dados["cnpj_beneficiario"] = buscar_regex(
                r':\s*(\d{1,2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}|\d{13,14})', pega_linha_abaixo)
            
        if "CNPJ Razão Social" in linha and i + 1 < total_linhas:
            dados["cnpj_pagador"] = buscar_regex(
                r'(\d{2}.?\d{3}.?\d{3}/?\d{4}-?\d{2}|\d{14})', pega_linha_abaixo)
            dados["pagador"] = buscar_regex(
                r'\d{2}.?\d{3}.?\d{3}/?\d{4}-?\d{2}\s+(.+)', pega_linha_abaixo)
  
        if "Documento de Arrecadação de Receitas Federais Pague com o PIX" in linha and len(linha) > 40:
            m = re.search(r'([\d\s]+)(?=\s*CNPJ:)', pega_linha_abaixo)
            if m:
                dados["linha_digitavel"] = m.group(1).strip()
            else:
                dados["linha_digitavel"] = None

    cnpj_chave = "24826317000140"
    if normalizar_cnpj_areal(dados["cnpj_beneficiario"]) == cnpj_chave:
        dados["tipo_operacao"] = "boleto de cobrança"
    elif normalizar_cnpj_areal(dados["cnpj_pagador"]) == cnpj_chave:
        dados["tipo_operacao"] = "pagamento de serviço/produto"
    else:
        dados["tipo_operacao"] = "outro"

    return dados
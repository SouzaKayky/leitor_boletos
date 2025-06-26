from utils.regex import buscar_regex
from utils.normalizar_cnpj import normalizar_cnpj_areal

def extrair_boleto_bb_v1(texto, dados):
    
    linhas = texto.splitlines()
    total_linhas = len(linhas)


    linhas = texto.splitlines()
    total_linhas = len(linhas)    
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()

        if i + 1 < total_linhas:
            pega_linha_abaixo = linhas[i + 1].strip()

        if "Vencimento" in linha and i + 1 < total_linhas:
            dados["vencimento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', pega_linha_abaixo)
        
        if "Data do documento" in linha and i + 1 < total_linhas:
            dados["data_documento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', pega_linha_abaixo)

        if "Data processamento" in linha and i + 1 < total_linhas:
            dados["data_processamento"] = buscar_regex(
                r'(\d{2}/\d{2}/\d{4})', pega_linha_abaixo)

        if "Número do documento" in linha and i + 1 < total_linhas:
            dados["numero_documento"] = buscar_regex(
                r'^([^\s]+)', pega_linha_abaixo)
            
        if "Nosso número/Código do Documento" in linha and i + 1 < total_linhas:
            dados["nosso_numero"] = buscar_regex(
                r'(\d{17})$', pega_linha_abaixo)
            
        if "(=) Valor cobrado" in linha and i + 1 < total_linhas:
            dados["valor_documento"] = buscar_regex(
                r'R?\$?\s*([\d\.,]+)', pega_linha_abaixo)

        if "Cedente Agência" in linha and i + 1 < total_linhas:
            dados["beneficiario"] = buscar_regex(
                r'^([A-Z\s]+)', pega_linha_abaixo)
            dados["cnpj_beneficiario"] = buscar_regex(
                r'(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})|24826317000140', pega_linha_abaixo)

        if linha.strip() == "Sacado" and i + 1 < total_linhas:
            for j in range(i + 1, min(i + 4, total_linhas)):  # olha no máximo 3 linhas abaixo
                linha_abaixo = linhas[j].strip()
                if "CPF/CNPJ:" in linha_abaixo:
                    dados["pagador"] = buscar_regex(
                        r'^(.*?)\s+CPF/CNPJ:', linha_abaixo
                    )
                    dados["cnpj_pagador"] = buscar_regex(
                        r'CPF/CNPJ:\s*(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})', linha_abaixo
                    )
                    break

        if "001-9" in linha and len(linha) > 40:
            dados["linha_digitavel"] = buscar_regex(
                r'(001-9[\d\. ]+)', linha)

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
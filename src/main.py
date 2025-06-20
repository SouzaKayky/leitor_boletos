import pdfplumber
import re
import pandas as pd
import sqlite3
from pathlib import Path

def buscar_regex(padrao, texto, grupo=1, padrao_padrao=""):
    resultado = re.search(padrao, texto, re.IGNORECASE)
    try:
        return resultado.group(grupo).strip()
    except:
        return padrao_padrao

def normalizar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

def extrair_dados_linha_a_linha(texto, nome_arquivo=""):
    dados = {
        "arquivo": nome_arquivo,
        "instituicao": "Sicredi (748-X)",
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

        if "Data de Processamento" in linha and i + 1 < total_linhas:
            dados["data_processamento"] = buscar_regex(r'(\d{2}/\d{2}/\d{4})', linhas[i+1])

        if "Valor do Documento" in linha and i + 1 < total_linhas:
            dados["valor_documento"] = buscar_regex(r'R\$?\s*([\d\.,]+)', linhas[i+1])

        if "Beneficiário CNPJ" in linha and i + 1 < total_linhas:
            linha_benef = linhas[i+1]
            dados["beneficiario"] = buscar_regex(r'^([A-Z\s]+)', linha_benef)
            dados["cnpj_beneficiario"] = buscar_regex(r'(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})|24826317000140', linha_benef)

        if re.search(r'^Pagador\s+', linha):
            dados["pagador"] = buscar_regex(r'^Pagador\s+([A-Z\s&\-.]+)\s+-', linha)
            dados["cnpj_pagador"] = buscar_regex(r'-\s*(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}|\d{14})', linha)

        if "748-X" in linha and len(linha) > 40:
            dados["linha_digitavel"] = buscar_regex(r'(748[\d\. ]+)', linha)

        # Captura número do documento e nosso número na mesma linha
        if re.search(r'\d{2}/\d{2}/\d{4}.*?DMI', linha):
            dados["numero_documento"] = buscar_regex(r'\d{2}/\d{2}/\d{4}\s+([0-9\-]+)', linha)
            dados["nosso_numero"] = buscar_regex(r'(\d{2}/\d{6}-\d|\d{2}/\d{6}-\d)', linha)

    # Classificação
    cnpj_chave = "24826317000140"
    if normalizar_cnpj(dados["cnpj_beneficiario"]) == cnpj_chave:
        dados["tipo_operacao"] = "boleto de cobrança"
    elif normalizar_cnpj(dados["cnpj_pagador"]) == cnpj_chave:
        dados["tipo_operacao"] = "pagamento de serviço/produto"
    else:
        dados["tipo_operacao"] = "outro"

    return dados

if __name__ == "__main__":
    pasta_data = Path("C:/Users/user/OneDrive/controle_administrativo_fox/financeiro/leitor_pdf_financeiro/data")
    pdfs = list(pasta_data.rglob("*.pdf"))

    todos_dados = []

    for caminho_pdf in pdfs:
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                texto = "\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
            dados_extraidos = extrair_dados_linha_a_linha(texto, nome_arquivo=caminho_pdf.name)
            todos_dados.append(dados_extraidos)
        except Exception as e:
            print(f"\nX - Erro ao processar {caminho_pdf.name}: {e}\n")

    if todos_dados:
        df = pd.DataFrame(todos_dados)

        # Garantir que a pasta exista
        pasta_data.mkdir(parents=True, exist_ok=True)

        # Salvar CSV
        caminho_csv = pasta_data / "dados_boletos.csv"
        df.to_csv(caminho_csv, index=False, encoding="utf-8")
        print(f"\nCSV salvo em: {caminho_csv}")

        # Salvar SQLite
        caminho_db = pasta_data / "dados_boletos.db"
        conn = sqlite3.connect(caminho_db)
        df.to_sql("boletos", conn, if_exists="replace", index=False)
        conn.close()
        print(f"Banco SQLite salvo em: {caminho_db}\n")

    else:
        print("\nX - Nenhum dado foi extraído.\n")

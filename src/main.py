import pdfplumber
import pandas as pd
import sqlite3
from pathlib import Path
from utils.construtor_extracao import extrair_dados

if __name__ == "__main__":
    pasta_data = Path("data")
    pdfs = list(pasta_data.rglob("*.pdf"))

    todos_dados = []

    for caminho_pdf in pdfs:
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                texto = "\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
            dados_extraidos =extrair_dados(texto, nome_arquivo=caminho_pdf.name)
            todos_dados.append(dados_extraidos)
        except Exception as e:
            print(f"\nX - Erro ao processar {caminho_pdf.name}: {e}\n")

    if todos_dados:
        df = pd.DataFrame(todos_dados)

        pasta_data.mkdir(parents=True, exist_ok=True)

        caminho_csv = pasta_data / "dados_boletos.csv"
        df.to_csv(caminho_csv, index=True, encoding="utf-8")
        print(f"\nCSV salvo em: {caminho_csv}")

        caminho_db = pasta_data / "dados_boletos.db"
        conn = sqlite3.connect(caminho_db)
        df.to_sql("boletos", conn, if_exists="replace", index=False)
        conn.close()
        print(f"Banco SQLite salvo em: {caminho_db}\n")

    else:
        print("\nX - Nenhum dado foi extraído.\n")

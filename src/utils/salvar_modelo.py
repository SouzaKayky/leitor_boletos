import os
from pathlib import Path
from config.settings import DATA_DIR

def salvar_texto_como_modelo(texto, nome_arquivo_pdf, layout="desconhecido"):

    pasta_destino = DATA_DIR / "modelos_layout" / layout

    pasta_destino.mkdir(parents=True, exist_ok=True)

    nome_txt = Path(nome_arquivo_pdf).stem + ".txt"
    caminho_txt = pasta_destino / nome_txt
    try:
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(texto)
    except Exception as e:
        print("!!! Erro ao salvar o arquivo:", e)


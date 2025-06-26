from utils.identificar_modelo_layout import identificar_layout
from utils.salvar_modelo import salvar_texto_como_modelo
from utils.cabecalho_tabela import cabecalho_tabela

from utils.scripts_models import *

def extrair_dados(texto, nome_arquivo=""):
    layout = identificar_layout(texto)
    salvar_texto_como_modelo(texto, nome_arquivo, layout)    

    dados = cabecalho_tabela(nome_arquivo, layout)
    
    if layout == "sicredi_v1":
        return extrair_boleto_sicredi_v1(texto, dados)
    elif layout == "sicredi_v2":
        return extrair_boleto_sicredi_v2(texto, dados)
    elif layout == "sicredi_v3":
        return extrair_boleto_sicredi_v3(texto, dados)
    elif layout == "bradesco_v1":
        return extrair_boleto_bradesco_v1(texto, dados)
    elif layout == "receita_federal_v1":
        return extrair_receita_federal_v1(texto, dados)  
    elif layout == "bb_v1":
        return extrair_boleto_bb_v1(texto, dados)
    # elif layout == "caixa":
    #     return extrair_dados_caixa(texto, nome_arquivo)
    else:
        return {"arquivo": nome_arquivo, "erro": "layout não reconhecido"}

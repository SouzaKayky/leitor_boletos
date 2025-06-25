# from utils.extracao_de_linhas import *
from utils.identificar_modelo_layout import identificar_layout
from utils.salvar_modelo import salvar_texto_como_modelo
from utils.scripts_models.sicredi_v1 import extrair_boleto_sicredi_v1
from utils.scripts_models.sicredi_v2 import extrair_boleto_sicredi_v2
from utils.scripts_models.sicredi_v3 import extrair_boleto_sicredi_v3

def extrair_dados(texto, nome_arquivo=""):
    layout = identificar_layout(texto)
    salvar_texto_como_modelo(texto, nome_arquivo, layout)    

    if layout == "sicredi_v1":
        return extrair_boleto_sicredi_v1(texto, nome_arquivo)
    elif layout == "sicredi_v2":
        return extrair_boleto_sicredi_v2(texto, nome_arquivo)
    elif layout == "sicredi_v3":
        return extrair_boleto_sicredi_v3(texto, nome_arquivo)
    # elif layout == "bb":
    #     return extrair_dados_bb(texto, nome_arquivo)
    # elif layout == "caixa":
    #     return extrair_dados_caixa(texto, nome_arquivo)
    else:
        return {"arquivo": nome_arquivo, "erro": "layout não reconhecido"}

import re 

def buscar_regex(padrao, texto, grupo=1, padrao_padrao=""):
    resultado = re.search(padrao, texto, re.IGNORECASE)
    try:
        return resultado.group(grupo).strip()
    except:
        return padrao_padrao
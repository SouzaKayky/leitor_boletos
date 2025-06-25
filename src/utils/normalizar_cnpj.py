import re

def normalizar_cnpj_areal(cnpj):
    return re.sub(r'\D', '', cnpj)
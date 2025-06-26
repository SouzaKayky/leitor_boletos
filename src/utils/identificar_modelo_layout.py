def identificar_layout(texto):
    
    texto_upper = texto.upper()
    
    if "SICREDI" in texto_upper or "748-X" in texto_upper:
        if "DETALHAMENTO DO BOLETO PARCELAS EM ABERTO" in texto_upper:
            return "sicredi_v3" 
        elif "CNPJ:" in texto and "CORTE NA LINHA ABAIXO" in texto_upper:
            return "sicredi_v2"  
        elif "RECIBO DO PAGADOR" in texto_upper:
            return "sicredi_v1"  
        else:
            return "sicredi_desconhecido"
    elif "Banco do Brasil" in texto or "001-9" in texto:
        return "bb_v1"
    elif "Caixa Econômica" in texto or "104-0" in texto:
        return "caixa"
    elif "Bradesco" in texto or "237-2" in texto:
        return "bradesco_v1"
    elif "Documento de Arrecadação" in texto or "24.826.317/0001-40" in texto:
        return "receita_federal_v1"
    elif "FGTS Digital" in texto: 
        return "fgts_digital"
    elif "Santander" in texto or "033-7" in texto:  
        return "santander"
    elif "Itaú" in texto or "341-7" in texto:
        return "itau"
    elif "sicoob" in texto or "756-" in texto:
        return "sicoob"
    else:
        return "desconhecido"

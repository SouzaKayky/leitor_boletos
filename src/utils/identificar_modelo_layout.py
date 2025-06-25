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
        return "bb"
    elif "Caixa Econômica" in texto or "104-0" in texto:
        return "caixa"
    elif "Bradesco" in texto or "237-2" in texto:
        return "bradesco"
    elif "Santander" in texto or "033-7" in texto:  
        return "santander"
    elif "Itaú" in texto or "341-7" in texto:
        return "itau"
    elif "sicoob" in texto or "756-8" in texto:
        return "sicoob"
    else:
        return "desconhecido"

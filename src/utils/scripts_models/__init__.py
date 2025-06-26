from .sicredi_v1 import extrair_boleto_sicredi_v1
from .sicredi_v2 import extrair_boleto_sicredi_v2
from .sicredi_v3 import extrair_boleto_sicredi_v3
from .bradesco_v1 import extrair_boleto_bradesco_v1
from .receita_federal_v1 import extrair_receita_federal_v1
from .bb_v1 import extrair_boleto_bb_v1

__all__ = [
    "extrair_boleto_sicredi_v1",
    "extrair_boleto_sicredi_v2",
    "extrair_boleto_sicredi_v3",
    "extrair_boleto_bradesco_v1",
    "extrair_boleto_bb_v1",
    "extrair_receita_federal_v1"
]

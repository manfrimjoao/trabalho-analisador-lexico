"""Grupo: RA1 - 23
Integrante: Joao Vitor Fernandes Manfrim (github manfrimjoao)
"""

from dataclasses import dataclass
from enum import Enum


class TokenType(str, Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    NUMERO_REAL = "NUMERO_REAL"
    OPERADOR = "OPERADOR"
    IDENT_MEM = "IDENT_MEM"
    KEYWORD_RES = "KEYWORD_RES"


@dataclass(frozen=True)
class Token:
    tipo: TokenType
    valor: str
    linha: int
    coluna: int

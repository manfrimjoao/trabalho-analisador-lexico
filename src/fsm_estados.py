"""Estados do AFD/FSM da análise léxica (sem regex)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .token_types import Token, TokenType

OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}


class LexicalError(ValueError):
    pass


@dataclass
class FSMContext:
    linha_texto: str
    numero_linha: int
    idx: int = 0
    tokens: list[Token] = field(default_factory=list)
    buffer: str = ""
    token_inicio: int = 0
    ponto_no_numero: bool = False
    paren_balance: int = 0

    def atual(self) -> str | None:
        if self.idx >= len(self.linha_texto):
            return None
        return self.linha_texto[self.idx]

    def avancar(self) -> None:
        self.idx += 1

    def adicionar(self, tipo: TokenType, valor: str, coluna: int | None = None) -> None:
        col = self.idx if coluna is None else coluna
        self.tokens.append(Token(tipo=tipo, valor=valor, linha=self.numero_linha, coluna=col + 1))


EstadoFn = Callable[[FSMContext], "EstadoFn | None"]


def estadoInicial(ctx: FSMContext) -> EstadoFn | None:
    c = ctx.atual()
    if c is None:
        return None

    if c in " \t\r\n":
        return estadoEspaco

    if c == "(":
        ctx.adicionar(TokenType.LPAREN, c)
        ctx.paren_balance += 1
        ctx.avancar()
        return estadoInicial

    if c == ")":
        ctx.adicionar(TokenType.RPAREN, c)
        ctx.paren_balance -= 1
        if ctx.paren_balance < 0:
            raise LexicalError(
                f"Linha {ctx.numero_linha}: parêntese fechado sem abertura na coluna {ctx.idx + 1}."
            )
        ctx.avancar()
        return estadoInicial

    if c.isdigit() or c == ".":
        ctx.buffer = ""
        ctx.token_inicio = ctx.idx
        ctx.ponto_no_numero = False
        return estadoNumero

    if c in "+-*/%^":
        ctx.buffer = ""
        ctx.token_inicio = ctx.idx
        return estadoOperador

    if c.isalpha() and c.isupper():
        ctx.buffer = ""
        ctx.token_inicio = ctx.idx
        return estadoIdentificador

    return estadoErro


def estadoEspaco(ctx: FSMContext) -> EstadoFn | None:
    while True:
        c = ctx.atual()
        if c is None or c not in " \t\r\n":
            return estadoInicial
        ctx.avancar()


def estadoNumero(ctx: FSMContext) -> EstadoFn | None:
    while True:
        c = ctx.atual()
        if c is None or c in " \t\r\n()+-*/%^":
            if ctx.buffer in {"", "."}:
                raise LexicalError(
                    f"Linha {ctx.numero_linha}: número malformado iniciado na coluna {ctx.token_inicio + 1}."
                )
            ctx.adicionar(TokenType.NUMERO_REAL, ctx.buffer, coluna=ctx.token_inicio)
            return estadoInicial

        if c == ",":
            raise LexicalError(
                f"Linha {ctx.numero_linha}: vírgula não é permitida em números na coluna {ctx.idx + 1}."
            )

        if c == ".":
            if ctx.ponto_no_numero:
                raise LexicalError(
                    f"Linha {ctx.numero_linha}: número malformado com mais de um ponto na coluna {ctx.idx + 1}."
                )
            ctx.ponto_no_numero = True
            ctx.buffer += c
            ctx.avancar()
            continue

        if c.isdigit():
            ctx.buffer += c
            ctx.avancar()
            continue

        raise LexicalError(
            f"Linha {ctx.numero_linha}: caractere inválido '{c}' em número na coluna {ctx.idx + 1}."
        )


def estadoOperador(ctx: FSMContext) -> EstadoFn | None:
    c = ctx.atual()
    if c is None:
        return estadoErro

    if c == "/":
        proximo_idx = ctx.idx + 1
        if proximo_idx < len(ctx.linha_texto) and ctx.linha_texto[proximo_idx] == "/":
            ctx.adicionar(TokenType.OPERADOR, "//", coluna=ctx.token_inicio)
            ctx.idx += 2
            return estadoInicial

    if c in OPERADORES:
        ctx.adicionar(TokenType.OPERADOR, c, coluna=ctx.token_inicio)
        ctx.avancar()
        return estadoInicial

    return estadoErro


def estadoIdentificador(ctx: FSMContext) -> EstadoFn | None:
    while True:
        c = ctx.atual()
        if c is None or c in " \t\r\n()+-*/%^":
            if not ctx.buffer:
                raise LexicalError(
                    f"Linha {ctx.numero_linha}: identificador vazio na coluna {ctx.token_inicio + 1}."
                )

            if ctx.buffer == "RES":
                ctx.adicionar(TokenType.KEYWORD_RES, ctx.buffer, coluna=ctx.token_inicio)
            else:
                ctx.adicionar(TokenType.IDENT_MEM, ctx.buffer, coluna=ctx.token_inicio)
            return estadoInicial

        if c.isalpha() and c.isupper():
            ctx.buffer += c
            ctx.avancar()
            continue

        if c.isdigit() and ctx.buffer:
            ctx.buffer += c
            ctx.avancar()
            continue

        raise LexicalError(
            f"Linha {ctx.numero_linha}: identificador inválido '{ctx.buffer + c}' na coluna {ctx.idx + 1}."
        )


def estadoErro(ctx: FSMContext) -> EstadoFn | None:
    c = ctx.atual()
    if c is None:
        raise LexicalError(f"Linha {ctx.numero_linha}: fim de linha inesperado.")
    raise LexicalError(
        f"Linha {ctx.numero_linha}: token inesperado '{c}' na coluna {ctx.idx + 1}."
    )

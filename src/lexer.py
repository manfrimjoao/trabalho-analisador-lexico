"""Módulo de análise léxica com FSM por funções."""

from __future__ import annotations

from .fsm_estados import FSMContext, LexicalError, estadoInicial
from .token_types import Token


def parseExpressao(linha: str, tokens: list[Token] | None = None, numero_linha: int = 1) -> list[Token]:
    """Realiza análise léxica de uma linha e retorna o vetor de tokens."""
    ctx = FSMContext(linha_texto=linha, numero_linha=numero_linha)
    estado = estadoInicial

    while estado is not None:
        estado = estado(ctx)

    if ctx.paren_balance != 0:
        raise LexicalError(
            f"Linha {numero_linha}: parênteses desbalanceados (saldo: {ctx.paren_balance})."
        )

    if tokens is not None:
        tokens.extend(ctx.tokens)
        return tokens

    return ctx.tokens

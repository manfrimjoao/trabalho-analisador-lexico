"""Infraestrutura de execução/validação para apoiar a geração de assembly."""

from __future__ import annotations

from dataclasses import dataclass, field

from .token_types import Token, TokenType


class ExecutionError(ValueError):
    pass


@dataclass
class ExecutionContext:
    memoria: dict[str, float] = field(default_factory=dict)
    historico: list[float] = field(default_factory=list)


def _aplicar_operador(a: float, b: float, op: str) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    if op == "//":
        return float(int(a) // int(b))
    if op == "%":
        return float(int(a) % int(b))
    if op == "^":
        if b < 0 or int(b) != b:
            raise ExecutionError("Expoente deve ser inteiro positivo em '^'.")
        return a ** int(b)
    raise ExecutionError(f"Operador não suportado: {op}")


def executarExpressao(tokens_linha: list[Token], contexto: ExecutionContext) -> float:
    """Executa de forma simples uma linha tokenizada para validar integridade do fluxo."""
    stack: list[float] = []

    for tk in tokens_linha:
        if tk.tipo in {TokenType.LPAREN, TokenType.RPAREN}:
            continue
        if tk.tipo == TokenType.NUMERO_REAL:
            stack.append(float(tk.valor))
            continue
        if tk.tipo == TokenType.IDENT_MEM:
            if len(stack) >= 1 and not any(t.tipo == TokenType.OPERADOR for t in tokens_linha):
                # Caso (V MEM): atribui o valor atual para MEM.
                valor = stack[-1]
                contexto.memoria[tk.valor] = valor
            stack.append(contexto.memoria.get(tk.valor, 0.0))
            continue
        if tk.tipo == TokenType.KEYWORD_RES:
            if not stack:
                raise ExecutionError("RES exige um índice N na pilha.")
            n = int(stack.pop())
            if n <= 0 or n > len(contexto.historico):
                raise ExecutionError(f"RES fora do histórico: {n}")
            stack.append(contexto.historico[-n])
            continue
        if tk.tipo == TokenType.OPERADOR:
            if len(stack) < 2:
                raise ExecutionError(f"Pilha insuficiente para operador {tk.valor}.")
            b = stack.pop()
            a = stack.pop()
            stack.append(_aplicar_operador(a, b, tk.valor))
            continue

    if not stack:
        resultado = 0.0
    else:
        resultado = stack[-1]

    contexto.historico.append(resultado)
    return resultado

"""Ponto de entrada do projeto RPN -> Tokens -> Assembly."""

from __future__ import annotations

import sys
from pathlib import Path

from .assembly_generator import gerarAssembly, salvarAssembly
from .executor import ExecutionContext, executarExpressao
from .io_arquivo import lerArquivo, salvarTokens
from .lexer import parseExpressao
from .token_types import Token


def exibirResultados(tokens_por_linha: list[list[Token]], resultados: list[float]) -> None:
    print("=== RESUMO DA EXECUÇÃO ===")
    for i, (tokens, resultado) in enumerate(zip(tokens_por_linha, resultados), start=1):
        tokens_txt = " ".join(f"{t.tipo.value}:{t.valor}" for t in tokens)
        print(f"Linha {i:02d} | Tokens: {tokens_txt}")
        print(f"Linha {i:02d} | Resultado infraestrutura: {resultado}")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Uso: python -m src.main <arquivo_entrada.txt>")
        return 1

    arquivo_entrada = args[0]
    linhas = lerArquivo(arquivo_entrada)

    tokens_por_linha: list[list[Token]] = []
    contexto_exec = ExecutionContext()
    resultados: list[float] = []

    for numero_linha, linha in enumerate(linhas, start=1):
        if not linha.strip():
            continue
        tokens_linha = parseExpressao(linha, numero_linha=numero_linha)
        tokens_por_linha.append(tokens_linha)
        resultados.append(executarExpressao(tokens_linha, contexto_exec))

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    salvarTokens(tokens_por_linha, str(output_dir / "tokens_ultima_execucao.txt"))

    codigo_asm = gerarAssembly(tokens_por_linha)
    salvarAssembly(codigo_asm, str(output_dir / "ultimo_assembly.s"))

    exibirResultados(tokens_por_linha, resultados)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

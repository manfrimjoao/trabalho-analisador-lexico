"""Entrada e saída de arquivos do projeto."""

from __future__ import annotations

from pathlib import Path

from .token_types import Token


def lerArquivo(nomeArquivo: str) -> list[str]:
    caminho = Path(nomeArquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {nomeArquivo}")
    return caminho.read_text(encoding="utf-8").splitlines()


def salvarTokens(tokens_por_linha: list[list[Token]], caminho_saida: str) -> None:
    linhas: list[str] = []
    for i, tokens in enumerate(tokens_por_linha, start=1):
        linhas.append(f"Linha {i}:")
        for tk in tokens:
            linhas.append(f"  ({tk.tipo.value}, '{tk.valor}', col={tk.coluna})")
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho_saida).write_text("\n".join(linhas) + "\n", encoding="utf-8")

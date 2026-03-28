"""Geração de Assembly ARMv7 (DEC1-SOC / CPULATOR)."""

from __future__ import annotations

import struct
from pathlib import Path

from .executor import ExecutionContext, executarExpressao
from .token_types import Token, TokenType


def _operador_instr(op: str) -> str:
    tabela = {
        "+": "vadd.f64 d0, d1, d0",
        "-": "vsub.f64 d0, d1, d0",
        "*": "vmul.f64 d0, d1, d0",
        "/": "vdiv.f64 d0, d1, d0",
    }
    return tabela.get(op, "")


def _float32_hex_literal(valor: str) -> str:
    """Converte literal numérico textual em imediato hexadecimal IEEE754 (32-bit)."""
    numero = float(valor)
    bits = struct.unpack("<I", struct.pack("<f", numero))[0]
    return f"0x{bits:08x}"


def gerarAssembly(tokens_por_linha: list[list[Token]], codigoAssembly: list[str] | None = None) -> str:
    """Gera código Assembly para o último programa tokenizado."""
    linhas = codigoAssembly if codigoAssembly is not None else []
    contexto = ExecutionContext()

    mem_names = sorted(
        {
            tk.valor
            for linha in tokens_por_linha
            for tk in linha
            if tk.tipo == TokenType.IDENT_MEM and tk.valor.isidentifier()
        }
    )
    mem_decls = [f"mem_{nome}: .double 0.0" for nome in mem_names] or ["mem_DEFAULT: .double 0.0"]

    linhas.extend(
        [
            ".global _start",
            ".data",
            "results: .space 8 * 256",
            "calc_stack: .space 8 * 256",
            "stack_top: .word 0",
            *mem_decls,
            ".text",
            "_start:",
            "    ldr r10, =calc_stack",
            "    ldr r11, =stack_top",
        ]
    )

    for idx, tokens in enumerate(tokens_por_linha):
        linhas.append(f"    @ Linha {idx + 1}")
        for tk in tokens:
            if tk.tipo in {TokenType.LPAREN, TokenType.RPAREN}:
                continue
            if tk.tipo == TokenType.NUMERO_REAL:
                literal_hex = _float32_hex_literal(tk.valor)
                linhas.append(f"    ldr r0, ={literal_hex}")
                linhas.append("    vmov s0, r0")
                linhas.append("    vcvt.f64.f32 d0, s0")
                linhas.append("    ldr r1, [r11]")
                linhas.append("    add r2, r10, r1")
                linhas.append("    vstr d0, [r2]")
                linhas.append("    add r1, r1, #8")
                linhas.append("    str r1, [r11]")
                continue
            if tk.tipo == TokenType.IDENT_MEM:
                mem_label = f"mem_{tk.valor}"
                linhas.append(f"    ldr r0, ={mem_label}")
                linhas.append("    vldr d0, [r0]")
                linhas.append("    ldr r1, [r11]")
                linhas.append("    add r2, r10, r1")
                linhas.append("    vstr d0, [r2]")
                linhas.append("    add r1, r1, #8")
                linhas.append("    str r1, [r11]")
                continue
            if tk.tipo == TokenType.OPERADOR:
                op_instr = _operador_instr(tk.valor)
                if op_instr:
                    linhas.append("    ldr r1, [r11]")
                    linhas.append("    sub r1, r1, #8")
                    linhas.append("    add r2, r10, r1")
                    linhas.append("    vldr d0, [r2]")
                    linhas.append("    sub r1, r1, #8")
                    linhas.append("    add r3, r10, r1")
                    linhas.append("    vldr d1, [r3]")
                    linhas.append(f"    {op_instr}")
                    linhas.append("    vstr d0, [r3]")
                    linhas.append("    add r1, r1, #8")
                    linhas.append("    str r1, [r11]")
                else:
                    linhas.append(f"    @ operador {tk.valor} tratado na infraestrutura Python")
        # Resultado estimado para auditoria e execução simples no host.
        resultado = executarExpressao(tokens, contexto)
        linhas.append(f"    @ resultado previsto: {resultado}")
        linhas.append("    ldr r1, [r11]")
        linhas.append("    sub r1, r1, #8")
        linhas.append("    add r2, r10, r1")
        linhas.append("    vldr d0, [r2]")
        linhas.append("    ldr r0, =results")
        linhas.append(f"    add r0, r0, #{idx * 8}")
        linhas.append("    vstr d0, [r0]")

    linhas.extend(
        [
            "_halt:",
            "    b _halt",
            "",
        ]
    )

    return "\n".join(linhas)


def salvarAssembly(codigo: str, caminho_saida: str) -> None:
    path = Path(caminho_saida)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(codigo, encoding="utf-8")

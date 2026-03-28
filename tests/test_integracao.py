import tempfile
import unittest
from pathlib import Path

from src.assembly_generator import gerarAssembly
from src.executor import ExecutionContext, executarExpressao
from src.io_arquivo import lerArquivo
from src.lexer import parseExpressao


class TestIntegracao(unittest.TestCase):
    def test_leitura_arquivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "entrada.txt"
            p.write_text("( 1 2 + )\n( 2 3 * )\n", encoding="utf-8")
            linhas = lerArquivo(str(p))
            self.assertEqual(len(linhas), 2)

    def test_execucao_res_mem(self):
        contexto = ExecutionContext()
        l1 = parseExpressao("( 10.0 M )", numero_linha=1)
        l2 = parseExpressao("( M )", numero_linha=2)
        l3 = parseExpressao("( 1 RES 5.0 + )", numero_linha=3)
        r1 = executarExpressao(l1, contexto)
        r2 = executarExpressao(l2, contexto)
        r3 = executarExpressao(l3, contexto)
        self.assertEqual(r1, 10.0)
        self.assertEqual(r2, 10.0)
        self.assertEqual(r3, 15.0)

    def test_gera_assembly(self):
        linhas = [
            parseExpressao("( 3.0 4.0 + )", numero_linha=1),
            parseExpressao("( 2.0 2.0 * )", numero_linha=2),
        ]
        asm = gerarAssembly(linhas)
        self.assertIn(".global _start", asm)
        self.assertIn("@ Linha 1", asm)


if __name__ == "__main__":
    unittest.main()

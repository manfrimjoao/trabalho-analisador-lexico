import unittest

from src.fsm_estados import LexicalError
from src.lexer import parseExpressao
from src.token_types import TokenType


class TestLexer(unittest.TestCase):
    def test_tokens_basicos(self):
        tokens = parseExpressao("( 3.14 2.0 + )", numero_linha=1)
        tipos = [t.tipo for t in tokens]
        self.assertEqual(
            tipos,
            [
                TokenType.LPAREN,
                TokenType.NUMERO_REAL,
                TokenType.NUMERO_REAL,
                TokenType.OPERADOR,
                TokenType.RPAREN,
            ],
        )

    def test_operador_divisao_inteira(self):
        tokens = parseExpressao("( 9 2 // )", numero_linha=2)
        self.assertEqual(tokens[3].valor, "//")

    def test_res_e_ident_mem(self):
        tokens = parseExpressao("( 2 RES A1 )", numero_linha=3)
        self.assertEqual(tokens[2].tipo, TokenType.KEYWORD_RES)
        self.assertEqual(tokens[3].tipo, TokenType.IDENT_MEM)

    def test_numero_malformado(self):
        with self.assertRaises(LexicalError):
            parseExpressao("( 3.14.5 2 + )", numero_linha=4)

    def test_parenteses_desbalanceados(self):
        with self.assertRaises(LexicalError):
            parseExpressao("( 3 2 +", numero_linha=5)


if __name__ == "__main__":
    unittest.main()

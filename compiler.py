
from lexer import Lexer
from parser import Parser
from validator import Validador


class Compiler:
    def compilar(self, codigo):
        tokens = Lexer(codigo).analizar()
        programa = Parser(tokens).analizar()

        Validador().validar_programa(programa)

        return programa

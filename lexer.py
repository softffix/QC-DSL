
from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    columna: int

    def __repr__(self):
        return (
            f"Token({self.tipo}, {self.valor!r}, "
            f"linea={self.linea}, columna={self.columna})"
        )


PALABRAS_RESERVADAS = {
    "producto", "parametro", "unidad", "minimo", "maximo",
    "regla", "cuando", "entonces", "aceptar", "rechazar",
    "alertar", "detener_linea", "y", "o"
}


class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []

    def actual(self):
        if self.posicion < len(self.codigo):
            return self.codigo[self.posicion]
        return None

    def avanzar(self):
        caracter = self.actual()

        if caracter is not None:
            self.posicion += 1
            if caracter == "\n":
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1

        return caracter

    def agregar(self, tipo, valor, linea, columna):
        self.tokens.append(Token(tipo, valor, linea, columna))

    def analizar(self):
        while self.actual() is not None:
            caracter = self.actual()

            if caracter in " \t\r":
                self.avanzar()
                continue

            if caracter == "\n":
                linea, columna = self.linea, self.columna
                self.avanzar()
                self.agregar("NEWLINE", "\n", linea, columna)
                continue

            if caracter == "#":
                while self.actual() is not None and self.actual() != "\n":
                    self.avanzar()
                continue

            if caracter == '"':
                self.leer_cadena()
                continue

            if caracter.isdigit():
                self.leer_numero()
                continue

            if caracter.isalpha() or caracter == "_":
                self.leer_identificador()
                continue

            if caracter in "<>!=":
                self.leer_operador()
                continue

            raise SyntaxError(
                f"Carácter no reconocido '{caracter}' "
                f"en línea {self.linea}, columna {self.columna}"
            )

        self.agregar("EOF", "", self.linea, self.columna)
        return self.tokens

    def leer_cadena(self):
        linea, columna = self.linea, self.columna
        self.avanzar()
        contenido = ""

        while self.actual() is not None:
            caracter = self.actual()

            if caracter == '"':
                self.avanzar()
                self.agregar("STRING", contenido, linea, columna)
                return

            if caracter == "\\":
                self.avanzar()
                siguiente = self.actual()

                if siguiente is None:
                    break

                traducciones = {
                    "n": "\n",
                    "t": "\t",
                    '"': '"',
                    "\\": "\\"
                }
                contenido += traducciones.get(siguiente, siguiente)
                self.avanzar()
                continue

            if caracter == "\n":
                raise SyntaxError(
                    f"Salto de línea dentro de una cadena, línea {linea}"
                )

            contenido += caracter
            self.avanzar()

        raise SyntaxError(
            f"Cadena sin cerrar en línea {linea}, columna {columna}"
        )

    def leer_numero(self):
        linea, columna = self.linea, self.columna
        numero = ""

        while self.actual() is not None and self.actual().isdigit():
            numero += self.avanzar()

        if (
            self.actual() == "."
            and self.posicion + 1 < len(self.codigo)
            and self.codigo[self.posicion + 1].isdigit()
        ):
            numero += self.avanzar()

            while self.actual() is not None and self.actual().isdigit():
                numero += self.avanzar()

        self.agregar("NUMBER", numero, linea, columna)

    def leer_identificador(self):
        linea, columna = self.linea, self.columna
        palabra = ""

        while self.actual() is not None and (
            self.actual().isalnum() or self.actual() == "_"
        ):
            palabra += self.avanzar()

        tipo = "KEYWORD" if palabra in PALABRAS_RESERVADAS else "IDENTIFIER"
        self.agregar(tipo, palabra, linea, columna)

    def leer_operador(self):
        linea, columna = self.linea, self.columna
        operador = self.avanzar()

        if self.actual() == "=":
            operador += self.avanzar()

        if operador not in {"<", ">", "<=", ">=", "==", "!="}:
            raise SyntaxError(f"Operador inválido: {operador}")

        self.agregar("OPERATOR", operador, linea, columna)

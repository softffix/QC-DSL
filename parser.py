
from ast_nodes import (
    Programa, Parametro, Regla,
    Condicion, CondicionLogica, Accion
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        return self.tokens[self.posicion]

    def avanzar(self):
        token = self.actual()
        if token.tipo != "EOF":
            self.posicion += 1
        return token

    def aceptar(self, tipo, valor=None):
        token = self.actual()

        if token.tipo == tipo and (valor is None or token.valor == valor):
            return self.avanzar()

        return None

    def esperar(self, tipo, valor=None):
        token = self.aceptar(tipo, valor)

        if token is None:
            esperado = valor if valor is not None else tipo
            encontrado = self.actual()

            raise SyntaxError(
                f"Se esperaba '{esperado}', pero se encontró "
                f"'{encontrado.valor}' en línea {encontrado.linea}"
            )

        return token

    def saltar_newlines(self):
        while self.actual().tipo == "NEWLINE":
            self.avanzar()

    def analizar(self):
        self.saltar_newlines()

        self.esperar("KEYWORD", "producto")
        producto = self.esperar("STRING").valor
        self.saltar_newlines()

        parametros = []
        while self.actual().valor == "parametro":
            parametros.append(self.leer_parametro())
            self.saltar_newlines()

        reglas = []
        while self.actual().valor == "regla":
            reglas.append(self.leer_regla())
            self.saltar_newlines()

        self.esperar("EOF")

        return Programa(producto, parametros, reglas)

    def leer_parametro(self):
        self.esperar("KEYWORD", "parametro")
        nombre = self.esperar("IDENTIFIER").valor
        self.esperar("KEYWORD", "unidad")
        unidad = self.esperar("STRING").valor
        self.esperar("KEYWORD", "minimo")
        minimo = float(self.esperar("NUMBER").valor)
        self.esperar("KEYWORD", "maximo")
        maximo = float(self.esperar("NUMBER").valor)

        return Parametro(nombre, unidad, minimo, maximo)

    def leer_regla(self):
        self.esperar("KEYWORD", "regla")
        nombre = self.esperar("STRING").valor

        self.esperar("NEWLINE")
        self.esperar("KEYWORD", "cuando")
        condicion = self.leer_condicion()

        self.esperar("NEWLINE")
        self.esperar("KEYWORD", "entonces")
        acciones = self.leer_acciones()

        return Regla(nombre, condicion, acciones)

    def leer_condicion(self):
        izquierda = self.leer_condicion_simple()

        while self.actual().valor in ("y", "o"):
            operador = self.avanzar().valor
            derecha = self.leer_condicion_simple()
            izquierda = CondicionLogica(izquierda, operador, derecha)

        return izquierda

    def leer_condicion_simple(self):
        parametro = self.esperar("IDENTIFIER").valor
        operador = self.esperar("OPERATOR").valor
        valor = float(self.esperar("NUMBER").valor)

        return Condicion(parametro, operador, valor)

    
    def leer_acciones(self):
        acciones = []

        while self.actual().tipo == "KEYWORD":
            palabra = self.actual().valor

            if palabra in {"aceptar", "rechazar"}:
                acciones.append(Accion(self.avanzar().valor))

            elif palabra == "detener_linea":
                self.avanzar()
                mensaje = self.esperar("STRING").valor
                acciones.append(Accion("detener_linea", mensaje))

            elif palabra == "alertar":
                self.avanzar()
                mensaje = self.esperar("STRING").valor
                acciones.append(Accion("alertar", mensaje))

            elif palabra == "y":
                self.avanzar()

            else:
                break

        return acciones


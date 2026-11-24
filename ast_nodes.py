
from dataclasses import dataclass


@dataclass
class Programa:
    producto: str
    parametros: list
    reglas: list


@dataclass
class Parametro:
    nombre: str
    unidad: str
    minimo: float
    maximo: float


@dataclass
class Regla:
    nombre: str
    condicion: object
    acciones: list


@dataclass
class Condicion:
    parametro: str
    operador: str
    valor: float


@dataclass
class CondicionLogica:
    izquierda: object
    operador: str
    derecha: object


@dataclass
class Accion:
    tipo: str
    mensaje: str = ""

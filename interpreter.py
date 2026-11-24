
class Interpreter:
    def __init__(self, programa):
        self.programa = programa

    def evaluar_condicion(self, condicion, mediciones):
        if hasattr(condicion, "parametro"):
            nombre = condicion.parametro

            if nombre not in mediciones:
                raise ValueError(
                    f"No se proporcionó la medición '{nombre}'."
                )

            valor = mediciones[nombre]
            operador = condicion.operador
            limite = condicion.valor

            operaciones = {
                "<": valor < limite,
                ">": valor > limite,
                "<=": valor <= limite,
                ">=": valor >= limite,
                "==": valor == limite,
                "!=": valor != limite
            }

            return operaciones[operador]

        izquierda = self.evaluar_condicion(
            condicion.izquierda, mediciones
        )
        derecha = self.evaluar_condicion(
            condicion.derecha, mediciones
        )

        if condicion.operador == "y":
            return izquierda and derecha

        if condicion.operador == "o":
            return izquierda or derecha

        raise ValueError("Operador lógico desconocido.")

    def ejecutar(self, mediciones):
        resultado = {
            "producto": self.programa.producto,
            "estado": "ACEPTADO",
            "alertas": [],
            "reglas_activadas": [],
            "linea_detenida": False
        }

        for regla in self.programa.reglas:
            if self.evaluar_condicion(regla.condicion, mediciones):
                resultado["reglas_activadas"].append(regla.nombre)

                for accion in regla.acciones:
                    if accion.tipo == "rechazar":
                        resultado["estado"] = "RECHAZADO"

                    elif accion.tipo == "aceptar":
                        pass

                    elif accion.tipo == "alertar":
                        resultado["alertas"].append(accion.mensaje)

                    elif accion.tipo == "detener_linea":
                        resultado["linea_detenida"] = True
                        resultado["estado"] = "RECHAZADO"
                        resultado["alertas"].append(accion.mensaje)

        return resultado

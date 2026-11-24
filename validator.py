
class Validador:
    def validar_programa(self, programa):
        errores = []

        if not programa.producto.strip():
            errores.append("El producto debe tener un nombre.")

        nombres = set()

        for parametro in programa.parametros:
            if parametro.nombre in nombres:
                errores.append(
                    f"El parámetro '{parametro.nombre}' está duplicado."
                )

            nombres.add(parametro.nombre)

            if parametro.minimo >= parametro.maximo:
                errores.append(
                    f"El mínimo de '{parametro.nombre}' debe ser "
                    "menor que su máximo."
                )

        for regla in programa.reglas:
            self.validar_condicion(regla.condicion, nombres, errores)

            if not regla.acciones:
                errores.append(
                    f"La regla '{regla.nombre}' no tiene acciones."
                )

            for accion in regla.acciones:
                if accion.tipo not in {
                    "aceptar", "rechazar", "alertar", "detener_linea"
                }:
                    errores.append(
                        f"Acción no válida: {accion.tipo}"
                    )

        if errores:
            raise ValueError("\n".join(errores))

        return True

    def validar_condicion(self, condicion, nombres, errores):
        if isinstance(condicion, type(None)):
            errores.append("Se encontró una condición vacía.")

        elif hasattr(condicion, "parametro"):
            if condicion.parametro not in nombres:
                errores.append(
                    f"El parámetro '{condicion.parametro}' "
                    "no ha sido declarado."
                )

        elif hasattr(condicion, "izquierda"):
            self.validar_condicion(
                condicion.izquierda, nombres, errores
            )
            self.validar_condicion(
                condicion.derecha, nombres, errores
            )

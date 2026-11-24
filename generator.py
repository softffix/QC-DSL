
class Generator:
    def generar(self, programa):
        lineas = [
            "# Código generado automáticamente por QC-DSL",
            "",
            f"PRODUCTO = {programa.producto!r}",
            "",
            "PARAMETROS = {"
        ]

        for p in programa.parametros:
            lineas.append(
                f"    {p.nombre!r}: "
                f"{{'unidad': {p.unidad!r}, "
                f"'minimo': {p.minimo}, 'maximo': {p.maximo}}},"
            )

        lineas.extend(["}", "", "# Reglas declaradas:"])

        for regla in programa.reglas:
            lineas.append(f"# - {regla.nombre}")

        lineas.extend([
            "",
            "def validar_mediciones(mediciones):",
            "    errores = []",
            "    for nombre, datos in PARAMETROS.items():",
            "        if nombre not in mediciones:",
            "            errores.append(f'Falta la medición: {nombre}')",
            "            continue",
            "        valor = mediciones[nombre]",
            "        if not datos['minimo'] <= valor <= datos['maximo']:",
            "            errores.append(f'{nombre} fuera de tolerancia')",
            "    return errores",
            ""
        ])

        return "\n".join(lineas)

# Código generado automáticamente por QC-DSL

PRODUCTO = 'Botella de plástico'

PARAMETROS = {
    'peso': {'unidad': 'g', 'minimo': 48.0, 'maximo': 52.0},
}

# Reglas declaradas:
# - Peso inferior
# - Peso excesivo
# - Control crítico

def validar_mediciones(mediciones):
    errores = []
    for nombre, datos in PARAMETROS.items():
        if nombre not in mediciones:
            errores.append(f'Falta la medición: {nombre}')
            continue
        valor = mediciones[nombre]
        if not datos['minimo'] <= valor <= datos['maximo']:
            errores.append(f'{nombre} fuera de tolerancia')
    return errores

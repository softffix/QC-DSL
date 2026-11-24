# QC-DSL – Sistema de Control de Calidad en Manufactura

## 1. Descripción del proyecto

QC-DSL es un lenguaje específico de dominio (DSL) desarrollado en Python para representar y simular reglas de control de calidad en procesos de manufactura.

Su propósito es permitir que el usuario defina parámetros de calidad, establezca límites de tolerancia y configure reglas para evaluar las mediciones de un producto.

El sistema permite determinar si un producto es aceptado o rechazado, generar alertas y simular la detención de una línea de producción.

## 2. Objetivos

- Desarrollar un lenguaje específico para el control de calidad.
- Definir parámetros y límites de tolerancia.
- Establecer reglas mediante condiciones lógicas.
- Interpretar las reglas y evaluar mediciones.
- Detectar errores en la definición del programa.
- Comprobar el funcionamiento mediante pruebas automatizadas.

## 3. Tecnologías utilizadas

- **Python 3.13:** lenguaje de programación principal.
- **Visual Studio Code:** entorno de desarrollo.
- **unittest:** herramienta para ejecutar pruebas automatizadas.

## 4. Estructura del proyecto

```text
QC-DSL/
│
├── examples/
│   └── botella.qcdsl
│
├── tests/
│   └── test_qcdsl.py
│
├── lexer.py
├── parser.py
├── ast_nodes.py
├── validator.py
├── interpreter.py
├── generator.py
├── compiler.py
├── main.py
├── codigo_generado.py
└── README.md
```

## 5. Componentes principales

| Archivo | Función |
|---|---|
| lexer.py | Reconoce los tokens del lenguaje. |
| parser.py | Analiza la estructura del programa. |
| ast_nodes.py | Define los nodos del árbol sintáctico. |
| validator.py | Comprueba la validez de las declaraciones y reglas. |
| compiler.py | Coordina las etapas de compilación. |
| interpreter.py | Evalúa las condiciones y ejecuta las acciones. |
| generator.py | Genera un archivo auxiliar de código Python. |
| main.py | Ejecuta el sistema. |
| test_qcdsl.py | Contiene las pruebas automatizadas. |

## 6. Sintaxis del lenguaje

Ejemplo de un programa escrito en QC-DSL:

```text
producto "Botella de plástico"

parametro peso unidad "g" minimo 48 maximo 52

regla "Peso inferior"
    cuando peso < 48
    entonces rechazar y alertar "Peso inferior al permitido"

regla "Peso excesivo"
    cuando peso > 52
    entonces rechazar y alertar "Peso superior al permitido"

regla "Control crítico"
    cuando peso < 48 o peso > 52
    entonces detener_linea "Producto fuera de tolerancia"
```

### Palabras reservadas

- `producto`: declara el producto.
- `parametro`: define una característica que será evaluada.
- `unidad`: establece la unidad de medición.
- `minimo` y `maximo`: establecen los límites permitidos.
- `regla`: declara una regla de control.
- `cuando`: define una condición.
- `entonces`: establece las acciones que se ejecutarán.
- `aceptar`: representa una acción de aceptación.
- `rechazar`: representa una acción de rechazo.
- `alertar`: genera una alerta.
- `detener_linea`: simula la detención de la línea de producción.
- `y` y `o`: permiten combinar condiciones lógicas.

## 7. Instalación y ejecución

### Requisitos

Tener Python instalado y disponible desde la terminal.

### Ejecutar el proyecto

Abrir una terminal en la carpeta principal del proyecto y ejecutar:

```powershell
python main.py
```

El sistema compilará el programa QC-DSL, evaluará las mediciones definidas y mostrará el resultado del control de calidad.

## 8. Pruebas automatizadas

El proyecto utiliza `unittest` para comprobar el funcionamiento de sus componentes principales.

Para ejecutar las pruebas:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas comprueban:

- Reconocimiento del producto.
- Aceptación de mediciones dentro del rango.
- Rechazo de mediciones fuera del rango.
- Cumplimiento de los límites mínimo y máximo.
- Detección de mediciones faltantes.

## 9. Alcance del proyecto

QC-DSL permite definir, compilar, validar e interpretar reglas de control de calidad mediante un lenguaje específico.

La detención de la línea de producción es una simulación lógica. El proyecto no controla maquinaria física ni está conectado a sistemas industriales PLC o SCADA.

## 10. Autor

**Anderson David Huamani Flores**

Proyecto académico – Ingeniería de Software.
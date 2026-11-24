
from pathlib import Path

from compiler import Compiler
from interpreter import Interpreter
from generator import Generator


def main():
    ruta = Path(__file__).parent / "examples" / "botella.qcdsl"

    codigo = ruta.read_text(encoding="utf-8")

    print("=" * 50)
    print("       SISTEMA DE CONTROL DE CALIDAD QC-DSL")
    print("=" * 50)

    try:
        programa = Compiler().compilar(codigo)

        print("\nCOMPILACIÓN EXITOSA")
        print("Producto:", programa.producto)
        print("Parámetros:", len(programa.parametros))
        print("Reglas:", len(programa.reglas))

        mediciones = {"peso": 50}

        print("\nMEDICIONES:")
        print(mediciones)

        resultado = Interpreter(programa).ejecutar(mediciones)

        print("\nRESULTADO DEL CONTROL:")
        print("Producto:", resultado["producto"])
        print("Estado:", resultado["estado"])
        print("Reglas activadas:", resultado["reglas_activadas"])
        print("Alertas:", resultado["alertas"])
        print("Línea detenida:", resultado["linea_detenida"])

        codigo_generado = Generator().generar(programa)

        salida = Path(__file__).parent / "codigo_generado.py"
        salida.write_text(codigo_generado, encoding="utf-8")

        print("\nCódigo Python generado en:", salida.name)

    except (SyntaxError, ValueError, KeyError) as error:
        print("\nERROR:", error)


if __name__ == "__main__":
    main()

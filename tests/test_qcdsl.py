
import unittest

from pathlib import Path
from compiler import Compiler
from interpreter import Interpreter


class TestQCDSL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ruta = (
            Path(__file__).parent.parent
            / "examples"
            / "botella.qcdsl"
        )

        codigo = ruta.read_text(encoding="utf-8")
        cls.programa = Compiler().compilar(codigo)

    def test_producto(self):
        self.assertEqual(
            self.programa.producto,
            "Botella de plástico"
        )

    def test_peso_aceptado(self):
        resultado = Interpreter(self.programa).ejecutar(
            {"peso": 50}
        )
        self.assertEqual(resultado["estado"], "ACEPTADO")

    def test_peso_inferior(self):
        resultado = Interpreter(self.programa).ejecutar(
            {"peso": 70}
        )
        self.assertEqual(resultado["estado"], "RECHAZADO")

    def test_peso_excesivo(self):
        resultado = Interpreter(self.programa).ejecutar(
            {"peso": 54}
        )
        self.assertEqual(resultado["estado"], "RECHAZADO")

    def test_limite_inferior(self):
        resultado = Interpreter(self.programa).ejecutar(
            {"peso": 48}
        )
        self.assertEqual(resultado["estado"], "ACEPTADO")

    def test_limite_superior(self):
        resultado = Interpreter(self.programa).ejecutar(
            {"peso": 52}
        )
        self.assertEqual(resultado["estado"], "ACEPTADO")

    def test_falta_medicion(self):
        with self.assertRaises(ValueError):
            Interpreter(self.programa).ejecutar({})


if __name__ == "__main__":
    unittest.main()

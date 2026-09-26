import unittest
from audit.logger import Auditor, IAuditWriter, IRelojProveedor


class WriterEnMemoria(IAuditWriter):
    """Doble de prueba: guarda las líneas en una lista en vez de un archivo."""
    def __init__(self):
        self.lineas = []

    def escribir(self, linea: str) -> None:
        self.lineas.append(linea)

    def leer_todo(self) -> str:
        return "\n".join(self.lineas)


class RelojFijo(IRelojProveedor):
    """Doble de prueba: siempre retorna la misma fecha/hora."""
    def ahora(self) -> str:
        return "2026-01-01 00:00:00"


class TestAuditor(unittest.TestCase):

    def setUp(self):
        self.writer = WriterEnMemoria()
        self.auditor = Auditor(writer=self.writer, reloj=RelojFijo())

    def test_registrar_evento(self):
        self.auditor.registrar("Servidor agregado: A")
        self.assertEqual(len(self.writer.lineas), 1)
        self.assertIn("Servidor agregado: A", self.writer.lineas[0])
        self.assertIn("2026-01-01 00:00:00", self.writer.lineas[0])

    def test_multiples_eventos(self):
        self.auditor.registrar("Evento 1")
        self.auditor.registrar("Evento 2")
        self.assertEqual(len(self.writer.lineas), 2)


if __name__ == "__main__":
    unittest.main()
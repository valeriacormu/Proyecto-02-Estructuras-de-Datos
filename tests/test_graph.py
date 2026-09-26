import unittest
from network.graph import Grafo, AuditorNulo


class TestGrafo(unittest.TestCase):

    def setUp(self):
        self.grafo = Grafo(auditor=AuditorNulo())
        self.grafo.agregar_conexion("A", "B", 4)
        self.grafo.agregar_conexion("A", "C", 1)
        self.grafo.agregar_conexion("C", "B", 2)
        self.grafo.agregar_conexion("B", "D", 5)
        self.grafo.agregar_conexion("C", "D", 8)

    def test_dijkstra_ruta_mas_corta(self):
        ruta, costo = self.grafo.calcular_ruta("A", "D")
        self.assertEqual(ruta, ["A", "C", "B", "D"])
        self.assertEqual(costo, 8)

    def test_dijkstra_sin_ruta(self):
        self.grafo.agregar_servidor("Aislado")
        ruta, costo = self.grafo.calcular_ruta("A", "Aislado")
        self.assertIsNone(ruta)
        self.assertEqual(costo, float("inf"))

    def test_diagnostico_detecta_aislado(self):
        self.grafo.agregar_servidor("Aislado")
        aislados = self.grafo.diagnostico_red()
        self.assertIn("Aislado", aislados)

    def test_eliminar_conexion(self):
        self.grafo.eliminar_conexion("A", "B")
        vecinos_a = [v for v, _ in self.grafo.adyacencia["A"]]
        self.assertNotIn("B", vecinos_a)

    def test_eliminar_servidor(self):
        self.assertTrue(self.grafo.eliminar_servidor("D"))
        self.assertNotIn("D", self.grafo.adyacencia)
        self.assertFalse(self.grafo.eliminar_servidor("Inexistente"))


if __name__ == "__main__":
    unittest.main()
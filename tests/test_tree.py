import unittest
from filesystem.tree import ArbolDirectorios, ILogger

class NullLogger(ILogger):
    def log(self, mensaje: str) -> None:
        pass

class TestArbolDirectorios(unittest.TestCase):
    def setUp(self):
        self.arbol = ArbolDirectorios(logger=NullLogger())

    def test_creacion_y_navegacion(self):
        self.assertTrue(self.arbol.crear_elemento("/", "home", es_carpeta=True))
        self.assertTrue(self.arbol.crear_elemento("/home", "user", es_carpeta=True))
        self.assertTrue(self.arbol.crear_elemento("/home/user", "script.py", es_carpeta=False, tamano=500))

        nodo = self.arbol.navegar_a_ruta("/home/user/script.py")
        self.assertIsNotNone(nodo)
        self.assertFalse(nodo.es_carpeta())
        self.assertEqual(nodo.obtener_tamano(), 500)

    def test_eliminar_en_cascada(self):
        self.arbol.crear_elemento("/", "var", es_carpeta=True)
        self.arbol.crear_elemento("/var", "log", es_carpeta=True)
        self.arbol.crear_elemento("/var/log", "syslog.txt", es_carpeta=False, tamano=200)

        self.assertTrue(self.arbol.eliminar_en_cascada("/var"))
        self.assertIsNone(self.arbol.navegar_a_ruta("/var/log/syslog.txt"))
        self.assertIsNone(self.arbol.navegar_a_ruta("/var"))

if __name__ == "__main__":
    unittest.main()
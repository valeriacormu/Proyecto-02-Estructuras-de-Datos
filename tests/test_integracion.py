import unittest
from audit.logger import Auditor, IAuditWriter, IRelojProveedor
from main import NetworkOS
from filesystem.tree import ArbolDirectorios, ILogger


class WriterEnMemoria(IAuditWriter):
    def __init__(self):
        self.lineas = []

    def escribir(self, linea: str) -> None:
        self.lineas.append(linea)

    def leer_todo(self) -> str:
        return "\n".join(self.lineas)


class RelojFijo(IRelojProveedor):
    def ahora(self) -> str:
        return "2026-01-01 00:00:00"


class NullLogger(ILogger):
    def log(self, mensaje: str) -> None:
        pass


class TestBusquedaRecursiva(unittest.TestCase):
    def test_buscar_encuentra_en_varias_ramas(self):
        a = ArbolDirectorios(logger=NullLogger())
        a.crear_elemento("/", "home", True)
        a.crear_elemento("/", "etc", True)
        a.crear_elemento("/home", "a.txt", False)
        a.crear_elemento("/etc", "a.txt", False)
        self.assertEqual(sorted(a.buscar_recursivo("a.txt")), ["/etc/a.txt", "/home/a.txt"])
        self.assertEqual(a.buscar_recursivo("nada"), [])


class TestNetworkOS(unittest.TestCase):
    def setUp(self):
        self.writer = WriterEnMemoria()
        self.net = NetworkOS(Auditor(self.writer, RelojFijo()))
        self.net.cargar_demo()

    def test_cada_servidor_tiene_su_propio_arbol_y_usuarios(self):
        self.assertIsNot(self.net.servidores["Heredia"].arbol, self.net.servidores["San Jose"].arbol)
        self.assertEqual(self.net.servidores["Heredia"].arbol.buscar_recursivo("informe.txt"), [])
        self.assertEqual(self.net.servidores["San Jose"].arbol.buscar_recursivo("informe.txt"),
                         ["/home/docs/informe.txt"])

    def test_login_exitoso_y_fallido_se_auditan(self):
        srv = self.net.servidores["San Jose"]
        self.assertTrue(srv.iniciar_sesion("admin", "admin123"))
        self.assertFalse(srv.iniciar_sesion("admin", "mala"))
        log = self.writer.leer_todo()
        self.assertIn("EXITOSO", log)
        self.assertIn("FALLIDO", log)

    def test_operaciones_de_arbol_se_auditan_en_archivo(self):
        srv = self.net.servidores["Heredia"]
        srv.arbol.crear_elemento("/", "tmp", True)
        self.assertIn("[Heredia] Creado Carpeta 'tmp'", self.writer.leer_todo())

    def test_ruta_dijkstra_demo(self):
        ruta, costo = self.net.grafo.calcular_ruta("Heredia", "Cartago")
        self.assertEqual(ruta, ["Heredia", "San Jose", "Cartago"])
        self.assertEqual(costo, 18)

    def test_eliminar_servidor_lo_quita_del_grafo(self):
        self.assertTrue(self.net.eliminar_servidor("Limon"))
        self.assertNotIn("Limon", self.net.grafo.adyacencia)
        self.assertNotIn("Limon", self.net.servidores)


if __name__ == "__main__":
    unittest.main()

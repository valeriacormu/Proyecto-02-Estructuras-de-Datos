import unittest
from filesystem.hash_table import TablaHashAutenticacion, PolynomialHashFunction


class TestTablaHashAutenticacion(unittest.TestCase):

    # Inicializamos la tabla hash con una capacidad pequeña para probar rehashing fácilmente
    def setUp(self):
        self.tabla = TablaHashAutenticacion(capacidad_inicial=5)

    # Valida la inserción y búsqueda de usuarios.
    def test_registro_y_autenticacion_exitosa(self):
        self.assertTrue(self.tabla.registrar_usuario("admin", "hash_password_123"))
        self.assertTrue(self.tabla.autenticar("admin", "hash_password_123"))

    # Valida que rechace contraseñas incorrectas o usuarios inexistentes.
    def test_autenticacion_fallida(self):

        self.tabla.registrar_usuario("user1", "pass_correcta")
        # Contraseña errónea
        self.assertFalse(self.tabla.autenticar("user1", "pass_incorrecta"))
        # Usuario no registrado
        self.assertFalse(self.tabla.autenticar("user_fantasma", "pass_correcta"))

    # Valida que no permita registrar dos veces el mismo nombre de usuario.
    def test_prevencion_usuarios_duplicados(self):
        self.assertTrue(self.tabla.registrar_usuario("dev_user", "pass1"))
        self.assertFalse(self.tabla.registrar_usuario("dev_user", "pass2"))
        
        # Debe conservar la primera contraseña registrada
        self.assertTrue(self.tabla.autenticar("dev_user", "pass1"))

    # Prueba que dos claves que generen el mismo índice se almacenen correctamente mediante Encadenamiento.
    def test_manejo_de_colisiones(self):

        # Forzamos una función hash fija o probamos con valores que colisionen
        class DummyHashFunction:
            def hash(self, clave: str, capacidad: int) -> int:
                return 1  # Todas las claves van al índice 1

        tabla_colision = TablaHashAutenticacion(capacidad_inicial=10, hash_fn=DummyHashFunction())
        
        self.assertTrue(tabla_colision.registrar_usuario("usuarioA", "passA"))
        self.assertTrue(tabla_colision.registrar_usuario("usuarioB", "passB"))
        
        # Ambos deben poder autenticarse a pesar de colisionar en el índice 1
        self.assertTrue(tabla_colision.autenticar("usuarioA", "passA"))
        self.assertTrue(tabla_colision.autenticar("usuarioB", "passB"))

    # Valida que al superar el factor de carga la tabla reajuste su capacidad al siguiente número primo.
    def test_rehashing_dinamico(self):
        capacidad_inicial = self.tabla.capacidad  # Capacidad inicial: 5
        
        # Insertamos suficientes elementos para superar el factor de carga (5 * 0.75 = 3.75)
        usuarios = [("user1", "p1"), ("user2", "p2"), ("user3", "p3"), ("user4", "p4")]
        for usr, pwd in usuarios:
            self.tabla.registrar_usuario(usr, pwd)

        # La capacidad debió aumentar al siguiente primo después de 5*2 = 10 -> 11
        self.assertGreater(self.tabla.capacidad, capacidad_inicial)
        self.assertEqual(self.tabla.tamano, 4)

        # Verificar que todos los usuarios sigan siendo accesibles tras la redistribución de claves
        for usr, pwd in usuarios:
            self.assertTrue(self.tabla.autenticar(usr, pwd))


if __name__ == "__main__":
    unittest.main()
"""
Network OS - Sistema de Archivos Distribuido y Enrutador de Red.
Menú interactivo que integra: árboles (filesystem), tabla hash (autenticación),
grafo (topología/Dijkstra/BFS) y auditoría (network_audit_log.txt).
"""

from typing import Dict, Optional

from audit.logger import Auditor
from network.graph import Grafo
from network.servidor import Servidor


class NetworkOS:
    def __init__(self, auditor: Optional[Auditor] = None):
        self.auditor = auditor or Auditor()
        self.grafo = Grafo(auditor=self.auditor)
        self.servidores: Dict[str, Servidor] = {}

    def agregar_servidor(self, nombre: str) -> bool:
        if nombre in self.servidores:
            self.grafo.agregar_servidor(nombre)  # registra el intento duplicado
            return False
        self.servidores[nombre] = Servidor(nombre, self.auditor)
        self.grafo.agregar_servidor(nombre)
        return True

    def eliminar_servidor(self, nombre: str) -> bool:
        if nombre not in self.servidores:
            return False
        self.grafo.eliminar_servidor(nombre)
        del self.servidores[nombre]
        return True

    def cargar_demo(self) -> None:
        for s in ("San Jose", "Heredia", "Alajuela", "Cartago", "Limon"):
            self.agregar_servidor(s)
            self.servidores[s].registrar_usuario("admin", "admin123")
        self.grafo.agregar_conexion("San Jose", "Heredia", 10)
        self.grafo.agregar_conexion("San Jose", "Alajuela", 15)
        self.grafo.agregar_conexion("Heredia", "Alajuela", 4)
        self.grafo.agregar_conexion("San Jose", "Cartago", 8)
        self.grafo.agregar_conexion("Cartago", "Limon", 30)
        arbol = self.servidores["San Jose"].arbol
        arbol.crear_elemento("/", "home", True)
        arbol.crear_elemento("/home", "docs", True)
        arbol.crear_elemento("/home/docs", "informe.txt", False, 120)
        arbol.crear_elemento("/", "etc", True)


# ---------------------------------------------------------------- utilidades
def pedir(msg: str) -> str:
    return input(msg).strip()


def pedir_float(msg: str) -> Optional[float]:
    try:
        valor = float(pedir(msg))
        return valor if valor >= 0 else None
    except ValueError:
        return None


def elegir_servidor(os_: NetworkOS, msg: str = "Servidor: ") -> Optional[Servidor]:
    nombre = pedir(msg)
    srv = os_.servidores.get(nombre)
    if srv is None:
        print(f"El servidor '{nombre}' no existe.")
    return srv


def listar_topologia(os_: NetworkOS) -> None:
    print("=== Topología de red ===")
    if not os_.grafo.adyacencia:
        print("(sin servidores)")
    for srv, vecinos in os_.grafo.adyacencia.items():
        con = ", ".join(f"{v} ({p}ms)" for v, p in vecinos) or "sin conexiones"
        print(f"  {srv}: {con}")


# ------------------------------------------------------------------- menús
def menu_servidor(os_: NetworkOS) -> None:
    """Sesión sobre un servidor: autenticación + operaciones del sistema de archivos."""
    srv = elegir_servidor(os_)
    if srv is None:
        return

    if not srv.iniciar_sesion(pedir("Usuario: "), pedir("Contraseña: ")):
        print("Credenciales inválidas.")
        return
    print(f"Sesión iniciada en {srv.nombre} como '{srv.sesion}'.")

    while True:
        print(f"\n--- {srv.nombre} ({srv.sesion}) ---")
        print("1. Mostrar árbol   2. Crear carpeta   3. Crear archivo")
        print("4. Buscar archivo  5. Eliminar (cascada)   6. Registrar usuario   0. Cerrar sesión")
        op = pedir("Opción: ")
        if op == "1":
            srv.arbol.mostrar_arbol()
        elif op == "2":
            ok = srv.arbol.crear_elemento(pedir("Ruta padre (ej. /home): "), pedir("Nombre: "), True)
            print("Carpeta creada." if ok else "No se pudo crear la carpeta.")
        elif op == "3":
            ruta, nombre = pedir("Ruta padre (ej. /home): "), pedir("Nombre: ")
            try:
                tam = int(pedir("Tamaño (bytes): ") or 0)
            except ValueError:
                tam = 0
            ok = srv.arbol.crear_elemento(ruta, nombre, False, tam)
            print("Archivo creado." if ok else "No se pudo crear el archivo.")
        elif op == "4":
            nombre = pedir("Nombre a buscar: ")
            rutas = srv.arbol.buscar_recursivo(nombre)
            srv._auditor.registrar(f"[{srv.nombre}] Búsqueda de '{nombre}': {len(rutas)} resultado(s)")
            print("\n".join(rutas) if rutas else "No encontrado.")
        elif op == "5":
            ok = srv.arbol.eliminar_en_cascada(pedir("Ruta a eliminar: "))
            print("Eliminado." if ok else "No se pudo eliminar.")
        elif op == "6":
            ok = srv.registrar_usuario(pedir("Nuevo usuario: "), pedir("Contraseña: "))
            print("Usuario registrado." if ok else "El usuario ya existe.")
        elif op == "0":
            srv.cerrar_sesion()
            return
        else:
            print("Opción inválida.")


def menu_principal(os_: NetworkOS) -> None:
    while True:
        print("\n===== NETWORK OS =====")
        print("1. Agregar servidor            2. Eliminar servidor")
        print("3. Agregar conexión            4. Eliminar conexión")
        print("5. Ver topología               6. Enviar paquete (Dijkstra)")
        print("7. Ping general (diagnóstico)  8. Acceder a un servidor (login)")
        print("9. Registrar usuario en servidor")
        print("10. Ver log de auditoría       11. Cargar red de ejemplo   0. Salir")
        op = pedir("Opción: ")

        if op == "1":
            nombre = pedir("Nombre del servidor: ")
            if not nombre or not os_.agregar_servidor(nombre):
                print("Nombre vacío o servidor ya existente.")
            else:
                os_.servidores[nombre].registrar_usuario("admin", "admin123")
                print(f"Servidor '{nombre}' creado (usuario inicial: admin / admin123).")
        elif op == "2":
            print("Eliminado." if os_.eliminar_servidor(pedir("Nombre: ")) else "No existe.")
        elif op == "3":
            a, b = pedir("Servidor A: "), pedir("Servidor B: ")
            peso = pedir_float("Latencia (ms): ")
            if a not in os_.servidores or b not in os_.servidores or a == b or peso is None:
                print("Datos inválidos (servidores deben existir, ser distintos y latencia >= 0).")
            else:
                os_.grafo.agregar_conexion(a, b, peso)
                print("Conexión procesada.")
        elif op == "4":
            ok = os_.grafo.eliminar_conexion(pedir("Servidor A: "), pedir("Servidor B: "))
            print("Conexión eliminada." if ok else "No existe esa conexión.")
        elif op == "5":
            listar_topologia(os_)
        elif op == "6":
            os_.grafo.imprimir_ruta(pedir("Servidor origen: "), pedir("Servidor destino: "))
        elif op == "7":
            os_.grafo.diagnostico_red()
        elif op == "8":
            menu_servidor(os_)
        elif op == "9":
            srv = elegir_servidor(os_)
            if srv:
                ok = srv.registrar_usuario(pedir("Nuevo usuario: "), pedir("Contraseña: "))
                print("Usuario registrado." if ok else "El usuario ya existe.")
        elif op == "10":
            os_.auditor.leer_log()
        elif op == "11":
            os_.cargar_demo()
            print("Red de ejemplo cargada (usuario admin / admin123 en cada servidor).")
        elif op == "0":
            print("Hasta luego.")
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    try:
        menu_principal(NetworkOS())
    except (EOFError, KeyboardInterrupt):
        print("\nSesión finalizada.")

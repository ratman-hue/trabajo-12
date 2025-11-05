import mysql.connector
import datetime
import hashlib

# Colores y formato para la salida (solo visual)
_OK = "\033[92m"      # verde
_ERROR = "\033[91m"   # rojo
_INFO = "\033[94m"    # azul
_WARN = "\033[93m"    # amarillo
_RESET = "\033[0m"

def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -------------------------------
# 🔌 CLASE CONEXIÓN BD (mensajes visuales cambiados)
# -------------------------------
class ConexionBD:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "toor"
        self.database = "biblioteca"
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexion.is_connected():
                print(f"{_OK}[{_timestamp()}] SUCCESS:{_RESET} Conexión establecida con la base de datos '{self.database}'.")
                return True
        except mysql.connector.Error as e:
            print(f"{_ERROR}[{_timestamp()}] ERROR:{_RESET} No se pudo conectar a la base de datos -> {e}")
            return False

    def desconectar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print(f"{_INFO}[{_timestamp()}] INFO:{_RESET} Conexión con la base de datos cerrada correctamente.")

    def ejecutar_consulta(self, consulta, parametros=None, fetch=False):
        try:
            if not self.conexion or not self.conexion.is_connected():
                if not self.conectar():
                    return None

            cursor = self.conexion.cursor()
            cursor.execute(consulta, parametros or ())

            if fetch:
                resultado = cursor.fetchall()
                cursor.close()
                return resultado
            else:
                self.conexion.commit()
                cursor.close()
                return True
        except mysql.connector.Error as e:
            print(f"{_ERROR}[{_timestamp()}] ERROR:{_RESET} Error ejecutando consulta -> {e}")
            return False

# -------------------------------
# 🔐 ENCRIPTACIÓN DE CONTRASEÑAS - (solo visual)
# -------------------------------
class Encriptador:
    @staticmethod
    def encriptar_contrasena(contrasena):
        """Encripta la contraseña usando SHA-256 (implementación internals no visual)."""
        return hashlib.sha256(contrasena.encode()).hexdigest()

    @staticmethod
    def verificar_contrasena(contrasena, hash_almacenado):
        """Verifica si la contraseña coincide con el hash"""
        return Encriptador.encriptar_contrasena(contrasena) == hash_almacenado

# -------------------------------
# 👤 CLASE USUARIO (cambios en textos visibles)
# -------------------------------
class Usuario:
    def __init__(self, nombre="", tipo="Estudiante", email="", contrasena="", id=None):
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo
        self.__email = email
        self.__contrasena_hash = Encriptador.encriptar_contrasena(contrasena) if contrasena else ""

    # GETTERS
    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo

    @property
    def email(self):
        return self.__email

    # SETTERS
    @nombre.setter
    def nombre(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__nombre = valor.strip()
        else:
            raise ValueError(f"{_ERROR}Nombre inválido{_RESET}")

    @tipo.setter
    def tipo(self, valor):
        tipos_validos = ["Estudiante", "Profesor", "Administrativo"]
        if valor in tipos_validos:
            self.__tipo = valor
        else:
            raise ValueError(f"{_ERROR}Tipo inválido. Debe ser: {', '.join(tipos_validos)}{_RESET}")

    def establecer_contrasena(self, contrasena):
        """Establece una nueva contraseña encriptada (solo visual del mensaje)."""
        if contrasena and len(contrasena) >= 4:
            self.__contrasena_hash = Encriptador.encriptar_contrasena(contrasena)
        else:
            raise ValueError(f"{_ERROR}La contraseña debe tener al menos 4 caracteres{_RESET}")

    def verificar_contrasena(self, contrasena):
        """Verifica si la contraseña es correcta"""
        return Encriptador.verificar_contrasena(contrasena, self.__contrasena_hash)

    def guardar_en_bd(self, conexion):
        """Guarda o actualiza un usuario en la base de datos (mensajes visuales)"""
        try:
            if self.__id is None:
                consulta = "INSERT INTO usuarios (nombre, tipo, email, contrasena_hash) VALUES (%s, %s, %s, %s)"
                parametros = (self.__nombre, self.__tipo, self.__email, self.__contrasena_hash)
            else:
                consulta = "UPDATE usuarios SET nombre=%s, tipo=%s, email=%s, contrasena_hash=%s WHERE id=%s"
                parametros = (self.__nombre, self.__tipo, self.__email, self.__contrasena_hash, self.__id)

            if conexion.ejecutar_consulta(consulta, parametros):
                print(f"{_OK}[{_timestamp()}] OK:{_RESET} Usuario '{self.__nombre}' guardado correctamente.")
                return True
            print(f"{_WARN}[{_timestamp()}] WARNING:{_RESET} No se pudo completar la operación de guardado.")
            return False
        except Exception as e:
            print(f"{_ERROR}[{_timestamp()}] ERROR:{_RESET} Excepción guardando usuario -> {e}")
            return False

    def __str__(self):
        return f"Usuario(id={self.__id}, nombre='{self.__nombre}', tipo='{self.__tipo}', email='{self.__email}')"

    # MÉTODOS DE CLASE
    @classmethod
    def obtener_por_id(cls, conexion, id_usuario):
        consulta = "SELECT id, nombre, tipo, email, contrasena_hash FROM usuarios WHERE id = %s"
        resultado = conexion.ejecutar_consulta(consulta, (id_usuario,), fetch=True)
        if resultado:
            id, nombre, tipo, email, contrasena_hash = resultado[0]
            usuario = cls(nombre, tipo, email, "", id)
            usuario.__contrasena_hash = contrasena_hash
            return usuario
        return None

    @classmethod
    def obtener_por_email(cls, conexion, email):
        consulta = "SELECT id, nombre, tipo, email, contrasena_hash FROM usuarios WHERE email = %s"
        resultado = conexion.ejecutar_consulta(consulta, (email,), fetch=True)
        if resultado:
            id, nombre, tipo, email, contrasena_hash = resultado[0]
            usuario = cls(nombre, tipo, email, "", id)
            usuario.__contrasena_hash = contrasena_hash
            return usuario
        return None

    @classmethod
    def obtener_todos(cls, conexion):
        consulta = "SELECT id, nombre, tipo, email, contrasena_hash FROM usuarios ORDER BY id"
        resultados = conexion.ejecutar_consulta(consulta, fetch=True)
        usuarios = []
        if resultados:
            for r in resultados:
                id, nombre, tipo, email, contrasena_hash = r
                usuario = cls(nombre, tipo, email, "", id)
                usuario.__contrasena_hash = contrasena_hash
                usuarios.append(usuario)
        return usuarios

# -------------------------------
# 📖 CLASE LIBRO (solo cambios visibles)
# -------------------------------
class Libro:
    def __init__(self, titulo="", autor="", anio=0, disponible=True, id=None):
        self.__id = id
        self.__titulo = titulo
        self.__autor = autor
        self.__anio = anio
        self.__disponible = disponible

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def disponible(self):
        return self.__disponible

    def guardar_en_bd(self, conexion):
        try:
            if self.__id is None:
                consulta = "INSERT INTO libros (titulo, autor, anio, disponible) VALUES (%s, %s, %s, %s)"
                parametros = (self.__titulo, self.__autor, self.__anio, self.__disponible)
            else:
                consulta = "UPDATE libros SET titulo=%s, autor=%s, anio=%s, disponible=%s WHERE id=%s"
                parametros = (self.__titulo, self.__autor, self.__anio, self.__disponible, self.__id)

            if conexion.ejecutar_consulta(consulta, parametros):
                print(f"{_OK}[{_timestamp()}] OK:{_RESET} Libro registrado: \"{self.__titulo}\" por {self.__autor}.")
                return True
            print(f"{_WARN}[{_timestamp()}] WARNING:{_RESET} No se pudo guardar el libro.")
            return False
        except Exception as e:
            print(f"{_ERROR}[{_timestamp()}] ERROR:{_RESET} Excepción guardando libro -> {e}")
            return False

    def __str__(self):
        estado = "Disponible" if self.__disponible else "Prestado"
        return f"Libro(id={self.__id}) - \"{self.__titulo}\" — {self.__autor} ({self.__anio}) [{estado}]"

    @classmethod
    def obtener_por_id(cls, conexion, id_libro):
        consulta = "SELECT id, titulo, autor, anio, disponible FROM libros WHERE id = %s"
        resultado = conexion.ejecutar_consulta(consulta, (id_libro,), fetch=True)
        if resultado:
            id, titulo, autor, anio, disponible = resultado[0]
            return cls(titulo, autor, anio, disponible, id)
        return None

    @classmethod
    def obtener_todos(cls, conexion):
        consulta = "SELECT id, titulo, autor, anio, disponible FROM libros ORDER BY id"
        resultados = conexion.ejecutar_consulta(consulta, fetch=True)
        libros = []
        if resultados:
            for r in resultados:
                id, titulo, autor, anio, disponible = r
                libros.append(cls(titulo, autor, anio, disponible, id))
        return libros

# -------------------------------
# 🔐 SISTEMA DE AUTENTICACIÓN (mensajes cambiados)
# -------------------------------
class SistemaAutenticacion:
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_usuario(self, nombre, tipo, email, contrasena):
        """Registra un nuevo usuario con contraseña encriptada"""
        try:
            usuario_existente = Usuario.obtener_por_email(self.conexion, email)
            if usuario_existente:
                print(f"{_WARN}[{_timestamp()}] WARNING:{_RESET} El correo '{email}' ya está registrado.")
                return False

            usuario = Usuario(nombre, tipo, email, contrasena)
            return usuario.guardar_en_bd(self.conexion)
        except Exception as e:
            print(f"{_ERROR}[{_timestamp()}] ERROR:{_RESET} Excepción registrando usuario -> {e}")
            return False

    def autenticar_usuario(self, email, contrasena):
        usuario = Usuario.obtener_por_email(self.conexion, email)
        if usuario and usuario.verificar_contrasena(contrasena):
            print(f"{_OK}[{_timestamp()}] AUTH:{_RESET} Acceso concedido. Bienvenido/a, {usuario.nombre}.")
            return usuario
        else:
            print(f"{_ERROR}[{_timestamp()}] AUTH FAIL:{_RESET} Credenciales inválidas.")
            return None

# -------------------------------
# ⚙ SISTEMA PRINCIPAL MEJORADO (texto visible cambiado)
# -------------------------------
class SistemaBiblioteca:
    def __init__(self):
        self.conexion_bd = ConexionBD()
        self.auth = SistemaAutenticacion(self.conexion_bd)
        self.usuario_actual = None

    def iniciar(self):
        header = [
            "+" + "-"*56 + "+",
            "|{:^56}|".format("SISTEMA DE GESTIÓN BIBLIOTECA"),
            "|{:^56}|".format("Conexión segura - Interfaz de consola"),
            "+" + "-"*56 + "+"
        ]
        print("\n".join(header))

        if not self.conexion_bd.conectar():
            return

        self.menu_autenticacion()
        self.conexion_bd.desconectar()

    def menu_autenticacion(self):
        """Menú de autenticación (texto del UI actualizado)"""
        while True:
            print("\n" + "-"*60)
            print("   Autenticación — Elija una opción")
            print("   1) Iniciar sesión")
            print("   2) Registrar usuario")
            print("   3) Salir")
            print("-"*60)
            opcion = input("   Seleccione (1/2/3): ").strip()

            if opcion == "1":
                email = input("   Correo electrónico: ").strip()
                contrasena = input("   Contraseña: ").strip()
                self.usuario_actual = self.auth.autenticar_usuario(email, contrasena)
                if self.usuario_actual:
                    self.menu_principal()
            elif opcion == "2":
                self.registrar_usuario()
            elif opcion == "3":
                print(f"{_INFO}Saliendo del sistema. Gracias por usar la aplicación.{_RESET}")
                break
            else:
                print(f"{_WARN}Opción inválida. Intente de nuevo.{_RESET}")

    def registrar_usuario(self):
        """Interfaz de registro (mensajes y prompts actualizados)"""
        print("\n--- REGISTRO DE NUEVO USUARIO ---")
        nombre = input("   Nombre completo: ").strip()
        tipo = input("   Tipo (Estudiante/Profesor/Administrativo): ").strip()
        email = input("   Correo electrónico: ").strip()
        contrasena = input("   Contraseña (mín. 4 caracteres): ").strip()

        if self.auth.registrar_usuario(nombre, tipo, email, contrasena):
            print(f"{_OK}Registro completado. Ya puede iniciar sesión con {email}.{_RESET}")

    def menu_principal(self):
        """Menú principal (texto visible y minimalista)"""
        while True:
            print("\n" + "="*60)
            print(f"  MENÚ PRINCIPAL  |  Usuario: {self.usuario_actual.nombre}  |  Tipo: {self.usuario_actual.tipo}")
            print("="*60)
            print("  1) Gestión de libros")
            print("  2) Listar usuarios")
            print("  3) Cerrar sesión")
            opcion = input("  Seleccione (1/2/3): ").strip()

            if opcion == "1":
                self.menu_libros()
            elif opcion == "2":
                self.listar_usuarios()
            elif opcion == "3":
                self.usuario_actual = None
                print(f"{_INFO}Sesión finalizada.{_RESET}")
                break
            else:
                print(f"{_WARN}Opción inválida.{_RESET}")

    def menu_libros(self):
        """Menú de gestión de libros (visual actualizado)"""
        while True:
            print("\n" + "-"*50)
            print("  GESTIÓN DE LIBROS")
            print("  1) Registrar libro")
            print("  2) Listar todos los libros")
            print("  3) Volver")
            print("-"*50)
            opcion = input("  Seleccione (1/2/3): ").strip()

            if opcion == "1":
                self.registrar_libro()
            elif opcion == "2":
                self.listar_libros()
            elif opcion == "3":
                break
            else:
                print(f"{_WARN}Opción inválida.{_RESET}")

    def registrar_libro(self):
        """Registro de libro (prompt y mensajes revisados)"""
        titulo = input("   Título: ").strip()
        autor = input("   Autor: ").strip()
        anio = datetime.datetime.now().year
        libro = Libro(titulo, autor, anio)
        if libro.guardar_en_bd(self.conexion_bd):
            print(f"{_OK}Libro '{titulo}' registrado ({anio}).{_RESET}")

    def listar_libros(self):
        """Listar libros (salida formateada)"""
        libros = Libro.obtener_todos(self.conexion_bd)
        if libros:
            print("\n--- LISTADO DE LIBROS ---")
            for libro in libros:
                print(f"  • {libro}")
        else:
            print(f"{_INFO}No se encontraron libros registrados.{_RESET}")

    def listar_usuarios(self):
        """Listar usuarios (salida formateada)"""
        usuarios = Usuario.obtener_todos(self.conexion_bd)
        if usuarios:
            print("\n--- LISTADO DE USUARIOS ---")
            for usuario in usuarios:
                print(f"  • {usuario}")
        else:
            print(f"{_INFO}No hay usuarios registrados.{_RESET}")

# -------------------------------
# 🏁 FUNCIÓN PRINCIPAL (sin cambios lógicos)
# -------------------------------
def main():
    sistema = SistemaBiblioteca()
    sistema.iniciar()

if __name__ == "__main__":
    main()

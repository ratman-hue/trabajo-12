# ■ Sistema de Gestión de Biblioteca (Consola)
Este proyecto es un **Sistema de Gestión de Biblioteca** desarrollado en Python con conexión a
MySQL, que permite:
■ Registrar y autenticar usuarios con contraseña encriptada
■ Gestionar libros: registrar y listar
■ Uso de SHA-256 para seguridad
■ Interfaz por consola con mensajes formateados
■ Organización del código con Programación Orientada a Objetos
---
## ■ Tecnologías Utilizadas
| Tecnología | Uso |
|------------|-----|
| Python 3.x | Lógica del sistema |
| MySQL Connector | Conexión a base de datos |
| MySQL | Persistencia de datos |
| SHA-256 + hashlib | Seguridad y cifrado de contraseñas |
---
## ■ Estructura del Código
El proyecto está compuesto por las siguientes clases:
| Clase | Función |
|--------|-----------|
| `ConexionBD` | Manejo de conexión, consultas y cierre de BD |
| `Usuario` | Modelo de usuario con validaciones y cifrado |
| `Libro` | Modelo para registrar y listar libros |
| `SistemaAutenticacion` | Registro e inicio de sesión |
| `SistemaBiblioteca` | Flujo general y menús |
---
## ■■ Tablas Requeridas en MySQL
Ejecutar antes de iniciar el sistema:
```sql
CREATE DATABASE biblioteca;
USE biblioteca;
CREATE TABLE usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
tipo VARCHAR(50) NOT NULL,
email VARCHAR(120) NOT NULL UNIQUE,
contrasena_hash VARCHAR(255) NOT NULL
);
CREATE TABLE libros (
id INT AUTO_INCREMENT PRIMARY KEY,
titulo VARCHAR(255) NOT NULL,
autor VARCHAR(255) NOT NULL,
anio INT NOT NULL,
disponible BOOLEAN DEFAULT TRUE
);
```
---
## ■■ ¿Cómo ejecutar?
### 1■■ Instalar dependencias
```bash
pip install mysql-connector-python
```
### 2■■ Configurar credenciales de MySQL
Modificar en la clase `ConexionBD` si es necesario:
```python
self.host = "localhost"
self.user = "root"
self.password = "toor"
self.database = "biblioteca"
```
### 3■■ Ejecutar el programa
```bash
python main.py
```
---
## ■ Flujo del Sistema
### ■ Inicio del programa
- Muestra bienvenida y se conecta a la BD
### ■ Menú de Autenticación
Opciones:
1. Iniciar sesión
2. Registrar usuario
3. Salir
### ■ Menú Principal
Solo accesible si el login es exitoso.
Permite:
- Gestión de libros
- Listar usuarios
- Cerrar sesión
---
## ■ Seguridad
✔ Contraseñas encriptadas con **SHA-256**
✔ No se guarda la contraseña en texto plano
✔ Validación de usuarios por correo electrónico
---
## ■ Mejoras Futuras Sugeridas
■ Rol de Administrador con permisos
■ Préstamos y devoluciones de libros
■ Reportes en PDF
■ Interfaz gráfica (Tkinter o Web)
---
## ■ Vista rápida del sistema
```text
+--------------------------------------------------------+
| SISTEMA DE GESTIÓN BIBLIOTECA |
| Conexión segura - Interfaz de consola |
+--------------------------------------------------------+
```
---

<img width="973" height="343" alt="Captura de pantalla 2025-11-05 103446" src="https://github.com/user-attachments/assets/9d62ddf8-89de-4e5c-881e-52fcd532b274" />


## ■■■ Autor
**Brandon**






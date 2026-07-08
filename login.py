from flask import Flask, request
import sqlite3
import hashlib


app = Flask(__name__)


# Crear base de datos

def crear_bd():

    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY,
        usuario TEXT,
        password TEXT
    )
    """)


    conexion.commit()

    conexion.close()



# Guardar usuario con contraseña hash

def crear_usuario(usuario, password):

    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()


    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()


    cursor.execute(
        "INSERT INTO usuarios(usuario,password) VALUES (?,?)",
        (usuario, password_hash)
    )


    conexion.commit()

    conexion.close()



# Validar usuario

def validar_usuario(usuario, password):

    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()


    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()


    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND password=?",
        (usuario, password_hash)
    )


    resultado = cursor.fetchone()


    conexion.close()


    if resultado:
        return True
    else:
        return False



@app.route("/", methods=["GET","POST"])
def inicio():

    mensaje = ""


    if request.method == "POST":

        usuario = request.form["usuario"]

        password = request.form["password"]


        if validar_usuario(usuario,password):

            mensaje = "Usuario válido"

        else:

            mensaje = "Usuario incorrecto"


    return """
    <h1>Login DRY7122</h1>

    <form method="POST">

    Usuario:
    <input name="usuario">

    <br>

    Contraseña:
    <input type="password" name="password">

    <br>

    <button type="submit">
    Ingresar
    </button>

    </form>

    <h3>
    """ + mensaje + """
    </h3>
    """



crear_bd()


# Usuarios del examen

crear_usuario("Lucas Alarcón","1234")



app.run(
    host="0.0.0.0",
    port=5800
)
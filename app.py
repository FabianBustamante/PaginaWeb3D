from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="impresiones_3d"
)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta del catálogo
@app.route('/catalogo')
def catalogo():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    return render_template('catalogo.html', productos=productos)

# Ruta para agregar productos (GET y POST)
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        cursor = db.cursor()
        query = "INSERT INTO productos (nombre, descripcion, precio) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, descripcion, precio))
        db.commit()

        return redirect(url_for('catalogo'))

    return render_template('agregar_producto.html')

# Ruta de contacto
@app.route('/contacto')
def contacto():
    return "Página de contacto."

# Ruta de login del administrador
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'contra123':
            return redirect(url_for('admin_dashboard'))
        else:
            return "Credenciales incorrectas."
    return render_template('admin_login.html')

# Ruta del dashboard del administrador
@app.route('/admin_dashboard')
def admin_dashboard():
    return "Bienvenido al panel de administrador."

if __name__ == '__main__':
    app.run(debug=True)

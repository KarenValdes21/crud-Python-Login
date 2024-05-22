from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'c81868cebd3d6044bc2e417c1bde5114'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'supermarket'

mysql = MySQL(app)


def check_credentials(username, password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM usuario WHERE username = %s AND contraseña = %s', (username, password))
    user = cursor.fetchone()
    return user

"""
    Endopints
"""
#########################################################################
# Home
#########################################################################
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_credentials(username, password)
        if user:
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            return "Credenciales incorrectas, intenta nuevamente"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


#########################################################################
# Clientes
#########################################################################
@app.route('/clientes')
def clientes():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, ClienteID, fechaCrea FROM cliente;")
        data = cur.fetchall()
        cur.close()
        return render_template('clientes.html', clientes=data)
    return redirect(url_for('login'))

@app.route('/clientes/<string:id_data>')
def clientes_delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.callproc('SP_EliminarCliente', [id_data])
    return redirect(url_for('clientes'))

@app.route('/clientes/add', methods = ['POST'])
def clientes_add():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        nombre_cliente = request.form['ClienteID']
        user_crea = session['user_id']
        cur = mysql.connection.cursor()
        cur.callproc('SP_AgregarCliente', [nombre_cliente, user_crea])
        mysql.connection.commit()
        return redirect(url_for('clientes'))

@app.route('/clientes/update', methods = ['POST'])
def clientes_update():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id = request.form['id']
        nombre_cliente = request.form['ClienteID']
        user_modifica = session['user_id']
        cur = mysql.connection.cursor()
        cur.callproc('SP_EditarCliente', [id, nombre_cliente, user_modifica])
        return redirect(url_for('clientes'))

#########################################################################
# Pedidos
#########################################################################
@app.route('/pedidos')
def pedidos():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT PedidoID, Precio, Cantidad, Descuento, Ganancia, OrdenFecha,EnvioFecha, ModoEnvio, idUsuarioModifica FROM pedido WHERE estatus = 1;")
        data = cur.fetchall()
        cur.close()
        return render_template('pedidos.html', pedidos=data)
    return redirect(url_for('login'))

@app.route('/pedidos/<string:id_data>')
def pedidos_delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.callproc('SP_EliminarPedido', [id_data])
    mysql.connection.commit()
    return redirect(url_for('pedidos'))

@app.route('/pedidos/add', methods = ['POST'])
def pedidos_add():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        idPedido = request.form['idPedido']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        descuento = request.form['descuento']
        ganancia = request.form['ganancia']
        fechaPedido = request.form['fechaPedido']
        fechaEnvio = request.form['fechaEnvio']
        modoEnvio = request.form['modoEnvio']
        cur = mysql.connection.cursor()
        cur.callproc('SP_AgregarPedido', [idPedido, precio, cantidad, descuento, ganancia, fechaPedido, fechaEnvio, modoEnvio])
        mysql.connection.commit()
        return redirect(url_for('pedidos'))

@app.route('/pedidos/update', methods = ['POST'])
def pedidos_update():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        idPedido = request.form['idPedido']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        descuento = request.form['descuento']
        ganancia = request.form['ganancia']
        fechaPedido = request.form['fechaPedido']
        fechaEnvio = request.form['fechaEnvio']
        modoEnvio = request.form['modoEnvio']
        usuario_modifica = session['user_id']
        cur = mysql.connection.cursor()
        cur.callproc('SP_EditarPedido', [idPedido,precio, cantidad, descuento, ganancia, fechaPedido, fechaEnvio, modoEnvio, usuario_modifica])
        mysql.connection.commit()
        return redirect(url_for('pedidos'))


#########################################################################
# Productos
#########################################################################
@app.route('/productos')
def productos():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT ProductoID, NombreProducto, idSubcategoria, fechaCrea, idUsuarioModifica FROM producto WHERE estatus = 1;")
        data = cur.fetchall()
        cur.close()
        return render_template('productos.html', productos=data)
    return redirect(url_for('login'))

@app.route('/productos/<string:id_data>')
def productos_delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.callproc('SP_EliminarProducto', [id_data])
    mysql.connection.commit()
    return redirect(url_for('productos'))

@app.route('/productos/add', methods = ['POST'])
def productos_add():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id = request.form['ProductoID']
        name = request.form['NombreProducto']
        usercreate = session['user_id']
        cur = mysql.connection.cursor()
        cur.callproc('SP_AgregarProducto', [id, name, usercreate])
        return redirect(url_for('productos'))

@app.route('/productos/update', methods = ['POST'])
def productos_update():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id = request.form['id']
        name = request.form['NombreProducto']
        userupdate = session['user_id']
        cur = mysql.connection.cursor()
        cur.callproc('SP_EditarProducto', [id, name, userupdate])
        #mysql.connection.commit()
        return redirect(url_for('productos'))








if __name__ == "__main__":
    app.run(debug=True)

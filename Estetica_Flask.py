from flask import Flask, render_template, request, redirect, url_for, flash

import pymysql.cursors

# Connect to the database
con = pymysql.connect(host='localhost',
                             user='root',
                             password='Urb@no1125',
                             db='Estetica',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__, template_folder="templates")

# Configuracion para Flash Messages
app.secret_key = "mysecretkey"
    
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Ventas',)
def ventas():
    return render_template('ventas.html')

@app.route('/Citas',)
def citas():
    return render_template('citas.html')

@app.route('/Clientes', methods=['GET'])
def clientes():
       return render_template('clientes.html')      

@app.route('/nuevo_cliente', methods = ['POST'])
def nuevo_cliente():
    Nombre_Cliente = request.form['Nombre_Cliente']
    Apellido_Cliente = request.form['Apellido_Cliente']
    Telefono_Cliente = request.form['Telefono_Cliente']
    Cumpleaños_Cliente = request.form['Cumpleaños_Cliente']
    cur = con.cursor()
    cur.execute("INSERT INTO Clientes2 (Nombre_Cliente, Apellido_Cliente, Telefono_Cliente, Cumpleanos_Cliente) VALUES (%s,%s,%s,%s)",(Nombre_Cliente, Apellido_Cliente, Telefono_Cliente, Cumpleaños_Cliente))
    con.commit()
    cur.close()
    flash('Cliente Agregado Correctamente')
    return redirect(url_for('clientes'))

@app.route('/Inventario', methods=['GET'])
def inventario():
    cur = con.cursor()
    cur.execute("SELECT * FROM Inventario2")
    Inventario = cur.fetchall()
    cur.close()
    return render_template('inventario.html', Inventario = Inventario)

@app.route('/inventario_form', methods=['GET'])
def inventario_form():
    return render_template('inventario_form.html')

@app.route('/nuevo_producto', methods=['POST'])
def nuevo_producto():
    Marca_Producto = request.form['Marca_Producto']
    Modelo_Producto = request.form['Modelo_Producto']
    Costo_Producto = request.form['Costo_Producto']
    Existencias = request.form['Existencias']
    cur = con.cursor()
    cur.execute("INSERT INTO Inventario2 (Marca_Producto, Modelo_Producto, Costo_Producto, Existencias) VALUES (%s,%s,%s,%s)",(Marca_Producto, Modelo_Producto, Costo_Producto, Existencias))
    con.commit()
    cur.close()
    flash('Producto Agregado Correctamente')
    return redirect(url_for('inventario'))   

@app.route('/editar_producto/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = con.cursor()
    cur.execute('SELECT * FROM Inventario2 WHERE ID_Producto = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('editar_producto.html', producto = data[0])

@app.route('/actualizar_producto/<id>', methods=['POST'])
def update_contact(id):
    Marca_Producto = request.form['Marca_Producto']
    Modelo_Producto = request.form['Modelo_Producto']
    Costo_Producto = request.form['Costo_Producto']
    Existencias = request.form['Existencias']
    cur = con.cursor()
    cur.execute("""
                UPDATE Inventario2 
                SET Marca_Producto = %s ,
                    Modelo_Producto = %s ,
                    Costo_Producto = %s ,
                    Existencias = %s
                WHERE ID_Producto = %s
                    """,(Marca_Producto, Modelo_Producto, Costo_Producto, Existencias, id))
    con.commit()
    cur.close()
    flash('Producto Editado Correctamente')
    return redirect(url_for('inventario'))

@app.route('/eliminar_producto/<id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = con.cursor()
    cur.execute('DELETE FROM Inventario2 WHERE ID_Producto = %s',(id))
    con.commit()
    flash('Producto Eliminado Correctamente')
    return redirect(url_for('inventario'))

if __name__ == '__main__':
    app.run(debug = True, port=8000)


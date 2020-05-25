from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors

app = Flask(__name__, template_folder="templates")

# Conexión a MySQL en Google Cloud
con = pymysql.connect(host='34.70.175.6',
                             user='root',
                             password='Urb@no1125',
                             db='Estetica',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


#Rutas de la App

@app.route('/index')
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('principal'))
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def inicio_sesion():
    user_login = request.form['user_login']
    pass_login = request.form['pass_login']

    cur = con.cursor()
    cur.execute("SELECT pass_login FROM Login WHERE user_login = %s",(user_login))
    user_pass_login = cur.fetchone()
    cur.close()
    if user_pass_login != None:
        if user_pass_login.get("pass_login") == pass_login:
            session['user'] = user_login
            return redirect(url_for('inventario'))
        else:
            flash("Contraseña Invalida")
            return redirect(url_for('index'))
    else:
        flash("Usuario No Encontrado")
        return redirect(url_for('index'))
    

@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/Principal')
def principal():
    if 'user' in session:
        return render_template('principal.html')
    else:
        return redirect(url_for('index'))

@app.route('/Ventas')
def ventas():
    if 'user' in session:
        return render_template('ventas.html')
    else:
        return redirect(url_for('index'))

@app.route('/Citas')
def citas():
    if 'user' in session:
        return render_template('citas.html')
    else:
        return redirect(url_for('index'))

@app.route('/Clientes', methods=['GET'])
def clientes():
    if 'user' in session:
        cur = con.cursor()
        cur.execute("SELECT * FROM Clientes2")
        Clientes = cur.fetchall()
        cur.close()
        return render_template('clientes.html', Clientes = Clientes)
    else:
        return redirect(url_for('index'))      


@app.route('/cliente_form', methods=['GET'])
def cliente_form():
    if 'user' in session:
        return render_template('clientes_form.html')
    else:
        return redirect(url_for('index'))


@app.route('/nuevo_cliente', methods = ['POST'])
def nuevo_cliente():
    if 'user' in session:
        Nombre_Cliente = request.form['Nombre_Cliente']
        Apellido_Cliente = request.form['Apellido_Cliente']
        Telefono_Cliente = request.form['Telefono_Cliente']
        Cumpleanos_Cliente = request.form['Cumpleanos_Cliente']
        cur = con.cursor()
        cur.execute("INSERT INTO Clientes2 (Nombre_Cliente, Apellido_Cliente, Telefono_Cliente, Cumpleanos_Cliente) VALUES (%s,%s,%s,%s)",(Nombre_Cliente, Apellido_Cliente, Telefono_Cliente, Cumpleanos_Cliente))
        con.commit()
        cur.close()
        flash('Cliente Agregado Correctamente')
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('index'))


@app.route('/editar_cliente/<id>', methods = ['POST', 'GET'])
def get_client(id):
    if 'user' in session:
        cur = con.cursor()
        cur.execute('SELECT * FROM Clientes2 WHERE ID_Cliente = %s', (id))
        data = cur.fetchall()
        cur.close()
        return render_template('editar_clientes.html', cliente = data[0])
    else:
        return redirect(url_for('index'))

@app.route('/actualizar_cliente/<id>', methods=['POST'])
def update_client(id):
    if 'user' in session:
        Nombre_Cliente = request.form['Nombre_Cliente']
        Apellido_Cliente = request.form['Apellido_Cliente']
        Telefono_Cliente = request.form['Telefono_Cliente']
        Cumpleanos_Cliente = request.form['Cumpleanos_Cliente']
        cur = con.cursor()
        cur.execute("""
                    UPDATE Clientes2 
                    SET Nombre_Cliente = %s ,
                        Apellido_Cliente = %s ,
                        Telefono_Cliente = %s ,
                        Cumpleanos_Cliente = %s
                    WHERE ID_Cliente = %s
                        """,(Nombre_Cliente, Apellido_Cliente, Telefono_Cliente, Cumpleanos_Cliente, id))
        con.commit()
        cur.close()
        flash('Producto Editado Correctamente')
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('index'))

@app.route('/eliminar_cliente/<id>', methods = ['POST','GET'])
def delete_client(id):
    if 'user' in session:
        cur = con.cursor()
        cur.execute('DELETE FROM Clientes2 WHERE ID_Cliente = %s',(id))
        con.commit()
        flash('Cliente Eliminado Correctamente')
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('index'))
        
#Propiedades del inventario
@app.route('/Inventario', methods=['GET'])
def inventario():
    if 'user' in session:
        cur = con.cursor()
        cur.execute("SELECT * FROM Inventario2")
        Inventario = cur.fetchall()
        cur.close()
        return render_template('inventario.html', Inventario = Inventario)
    else:
        return redirect(url_for('index'))

@app.route('/inventario_form', methods=['GET'])
def inventario_form():
    if 'user' in session:
        return render_template('inventario_form.html')
    else:
        return redirect(url_for('index'))

@app.route('/nuevo_producto', methods=['POST'])
def nuevo_producto():
    if 'user' in session:
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
    else:
        return redirect(url_for('index'))   

@app.route('/editar_producto/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    if 'user' in session:
        cur = con.cursor()
        cur.execute('SELECT * FROM Inventario2 WHERE ID_Producto = %s', (id))
        data = cur.fetchall()
        cur.close()
        return render_template('editar_producto.html', producto = data[0])
    else:
        return redirect(url_for('index'))

@app.route('/actualizar_producto/<id>', methods=['POST'])
def update_contact(id):
    if 'user' in session:
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
    else:
        return redirect(url_for('index'))

@app.route('/eliminar_producto/<id>', methods = ['POST','GET'])
def delete_contact(id):
    if 'user' in session:
        cur = con.cursor()
        cur.execute('DELETE FROM Inventario2 WHERE ID_Producto = %s',(id))
        con.commit()
        flash('Producto Eliminado Correctamente')
        return redirect(url_for('inventario'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Configuracion para Flash Messages
    app.secret_key = "mysecretkey"
    app.run(debug = True, port=8000)
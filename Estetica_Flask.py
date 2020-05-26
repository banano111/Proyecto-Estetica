from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
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

lista = []
Suma = 0

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
    

@app.route('/agregar_admin', methods=['POST', 'GET'])
def add_admin():
    if 'user' in session:
        if request.method == "POST":
            user_login = request.form['user_login']
            pass_login = request.form['pass_login']
            cur = con.cursor()
            cur.execute("INSERT INTO Login (user_login, pass_login) VALUES (%s, %s)", (user_login, pass_login))
            con.commit()
            cur.close()
            return redirect(url_for('principal'))
        else:
            return render_template('agregar_admin.html')
    else:
        return redirect(url_for('index'))

@app.route('/cambiar_contrasena', methods=['POST', 'GET'])
def cambiar_password():
    if 'user' in session:
        if request.method == "POST":
            Nueva_Contrasena = request.form['Nueva_Contrasena']
            cur = con.cursor()
            cur.execute("UPDATE Login SET pass_login = %s WHERE user_login = %s",(Nueva_Contrasena,session['user']))
            con.commit()
            cur.close()
            session.clear()
            return redirect(url_for('index'))
        else:
            return render_template('cambiar_contrasena.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/Ventas')
def ventas():
    if 'user' in session:
        global Suma
        Suma = 0
        lista.clear()
        cur = con.cursor()
        cur.execute("SELECT Servicios FROM CAT_Servicios")
        Servicios =  cur.fetchall()
        cur.close()
        return render_template('ventas.html', Servicios = Servicios)
    else:
        return redirect(url_for('index'))


@app.route('/nueva_venta', methods=['POST'])
def nueva_venta():
    if 'user' in session:
        global Suma
        TotalF = 0
        ban = 1
        Servicio_Venta = request.form['Producto_servicio']
        Cantidad_Servicio = request.form['Cantidad_Ventas']
        cur = con.cursor()
        cur.execute("SELECT Servicios FROM CAT_Servicios")
        Servicios =  cur.fetchall()
        cur.execute("SELECT Precio FROM CAT_Servicios WHERE Servicios = %s", Servicio_Venta)
        Precio_Serv = cur.fetchall()
        cur.close()
        for pre in Precio_Serv:
            Precio_F = int(pre['Precio'])
        TotalF = Precio_F * int(Cantidad_Servicio)    
        lista.append({'Serv_Ven': Servicio_Venta, 'Cant': Cantidad_Servicio, 'Precio': Precio_F, 'PrecioTotal': TotalF})
        print(TotalF)
        print(Suma)
        Suma = TotalF + Suma
        print(lista)
        return render_template('ventas.html', Servicios = Servicios, lista = lista, Suma_Total = Suma, ban = ban)
    else:
        return redirect(url_for('index'))

@app.route('/generar_venta', methods=['POST'])
def generar_venta():
    if 'user' in session:
        hoy = date.today()
        print(hoy)
        global Suma
        cur = con.cursor()
        cur.execute("INSERT INTO Ventas (Fecha_Venta, Total) VALUES (%s,%s)",(hoy,Suma))
        con.commit()
        cur.close()
        flash('Venta Generada Con Exito')
        return redirect(url_for('ventas'))
    else:
        return redirect(url_for('index'))

@app.route('/registro_ventas')
def registro_ventas():
    if 'user' in session:
        cur = con.cursor()
        cur.execute("SELECT * FROM Ventas")
        Ventas =  cur.fetchall()
        cur.close()
        return render_template('registro_ventas.html', Ventas = Ventas)
    else:
        return redirect(url_for('index'))

@app.route('/Citas')
def citas():
    if 'user' in session:
        cur = con.cursor()
        cur.execute("SELECT * FROM Citas")
        Citas = cur.fetchall()
        cur.execute("SELECT Servicios FROM CAT_Servicios")
        Servicios =  cur.fetchall()
        cur.close()
        return render_template('citas.html', Citas = Citas, Servicios = Servicios)
    else:
        return redirect(url_for('index'))

@app.route('/nueva_cita', methods=['POST'])
def nueva_cita():
    if 'user' in session:
        Fecha_Cita = request.form['Fecha_Cita']
        Cliente_Cita = request.form['Cliente_Cita']
        Hora_Cita = request.form['Horario_Cita']
        ID_Servicio = request.form['Servicio_Cita']
        cur = con.cursor()
        cur.execute("INSERT INTO Citas (Fecha_Cita, ID_Servicios, ID_Cliente, Hora_Cita) VALUES (%s,%s,%s,%s)",(Fecha_Cita,ID_Servicio,Cliente_Cita,Hora_Cita))
        con.commit()
        cur.close()
        flash('Nueva Cita Agregada')
        return redirect(url_for('citas'))
    else:
        return redirect(url_for('index'))

@app.route('/editar_cita/<id>')
def editar_cita(id):
    if 'user' in session:
        cur = con.cursor()
        cur.execute('SELECT * FROM Citas WHERE ID_Cita = %s', (id))
        data = cur.fetchall()
        cur.execute("SELECT Servicios FROM CAT_Servicios")
        Servicios =  cur.fetchall()
        cur.close()
        return render_template('editar_cita.html', cita = data[0], Servicios = Servicios)
    else:
        return redirect(url_for('index'))

@app.route('/actualizar_cita/<id>', methods=['POST'])
def update_cita(id):
    if 'user' in session:
        Fecha_Cita = request.form['Fecha_Cita']
        Cliente_Cita = request.form['Cliente_Cita']
        Hora_Cita = request.form['Horario_Cita']
        ID_Servicio = request.form['Servicio_Cita']
        cur = con.cursor()
        cur.execute("""
                    UPDATE Citas
                    SET Fecha_Cita = %s ,
                        ID_Cliente = %s ,
                        Hora_Cita = %s ,
                        ID_Servicios = %s
                    WHERE ID_Cita = %s
                        """,(Fecha_Cita,Cliente_Cita,Hora_Cita,ID_Servicio,id))
        con.commit()
        cur.close()
        flash('Cita Editada Correctamente')
        return redirect(url_for('citas'))
    else:
        return redirect(url_for('index'))

@app.route('/eliminar_cita/<id>')
def eliminar_citas(id):
    if 'user' in session:
        cur = con.cursor()
        cur.execute('DELETE FROM Citas WHERE ID_Cita = %s',(id))
        con.commit()
        flash('Cita Eliminada Correctamente')
        return redirect(url_for('citas'))
    else:
        return redirect(url_for('index'))

@app.route('/Clientes', methods=['GET'])
def clientes():
    if 'user' in session:
        cur = con.cursor()
        cur.execute("SELECT * FROM Clientes2")
        Clientes = cur.fetchall()
        cur.close()
        print(Clientes)
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
    app.run(host='0.0.0.0', port=80)
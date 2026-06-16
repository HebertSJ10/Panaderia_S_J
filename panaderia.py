from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'panaderia_sanjuan_premium_upn'

# =========================================================================
# 1. DATA EN MEMORIA (Listas dinámicas mutables)
# =========================================================================
productos = [
    {"id": 1, "nombre": "Pan Francés", "descripcion": "Tradicional y crujiente.", "precio": 0.20, "imagen": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?q=80&w=400"},
    {"id": 2, "nombre": "Pan Chabata", "descripcion": "Pan artesanal rústico.", "precio": 0.30, "imagen": "https://www.panaderiaalemana.com/wp-content/uploads/2020/11/Pan-ciabatta.jpg"},
    {"id": 3, "nombre": "Pan de Molde", "descripcion": "Suave y para sándwich.", "precio": 7.50, "imagen": "https://images.unsplash.com/photo-1598373182133-52452f7691ef?q=80&w=400"},
    {"id": 4, "nombre": "Torta de Chocolate", "descripcion": "Cacao puro nacional.", "precio": 40.00, "imagen": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=400"},
    {"id": 5, "nombre": "Cachito Mantequilla", "descripcion": "Suave y tradicional.", "precio": 0.50, "imagen": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=400"},
    {"id": 6, "nombre": "Pan Baguette", "descripcion": "Largo y muy crocante.", "precio": 3.00, "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9SwWuaLPjSZbZR5ouyneVKiCxXvpfymLuEw&s"},
    {"id": 7, "nombre": "Empanada Carne", "descripcion": "Relleno clásico criollo.", "precio": 5.00, "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3AL1iExIyFoi3WvX3n6UzihA6QNU9aY5bUg&s"},
    {"id": 8, "nombre": "Torta Helada", "descripcion": "Bizcocho con gelatina.", "precio": 30.00, "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpJwuvsuCh-r63wUnZBMlU4Twbft-DMqZ1bg&s"}
]

servicios = [
    {"id": 1, "nombre": "Catering para Eventos", "descripcion": "Bandejas surtidas de bocaditos salados y dulces.", "precio": 150.00},
    {"id": 2, "nombre": "Buffet de Desayuno Criollo", "descripcion": "Chicharrón, tamales y pan caliente.", "precio": 250.00}
]

clientes = [
    {"id": 1, "nombre": "Santi Mendoza", "email": "santi.mendoza@email.com", "telefono": "987654321"}
]

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# =========================================================================
# 2. PLANTILLA HTML PRINCIPAL (Portal del Cliente)
# =========================================================================
HTML_PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panadería San Juan</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #121212; color: #e0e0e0; }
        header { background-color: #634832; color: white; padding: 15px; border-radius: 8px; }
        nav ul { list-style: none; padding: 0; margin: 0; }
        nav ul li { display: inline; margin: 0 10px; }
        nav ul li a { color: white; text-decoration: none; font-weight: bold; cursor: pointer; }
        
        .seccion-contenido { display: block; }
        .oculto { display: none !important; }

        .contenedor-tarjetas { display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap; }
        .tarjeta { background: #1e1e1e; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); flex: 1; min-width: 250px; }
        
        .contenedor-buscador { text-align: center; margin: 20px 0; }
        .input-buscador { width: 60%; max-width: 500px; padding: 12px 20px; font-size: 1rem; border-radius: 25px; border: 1px solid #444; background-color: #1e1e1e; color: #fff; outline: none; }

        .catalogo-grid { display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap; }
        .producto-card { background: #1e1e1e; padding: 15px; border-radius: 8px; width: calc(25% - 15px); box-sizing: border-box; text-align: center; min-width: 230px; }
        .producto-card img { width: 100%; height: 160px; border-radius: 6px; object-fit: cover; }
        .precio { display: block; font-weight: bold; color: #28a745; font-size: 1.2rem; margin-bottom: 15px; }
        .btn-consultar { background-color: #634832; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; width: 100%; text-transform: uppercase; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #1e1e1e; }
        th { background: #634832; padding: 12px; color: white; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #333; }

        .contacto-simple { margin-top: 40px; background: #1e1e1e; padding: 25px; border-radius: 8px; }
        .info-contacto { display: flex; gap: 30px; margin-top: 15px; font-size: 1.1rem; flex-wrap: wrap; justify-content: space-around; }
        .info-contacto div { background: #252525; padding: 15px 20px; border-radius: 6px; text-align: center; }
        .info-contacto i { color: #28a745; font-size: 1.3rem; }
        
        form label { font-weight: bold; display: block; margin-top: 10px; color: #ddd; }
        form input[type="text"], form input[type="password"], form input[type="number"] { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #444; background-color: #2d2d2d; color: #fff; border-radius: 4px; box-sizing: border-box; }
        
        .contenedor-admin-centrado { display: flex; justify-content: center; align-items: center; min-height: 60vh; width: 100%; }
        .tarjeta-admin-medio { background: #1e1e1e; padding: 30px; border-radius: 12px; width: 100%; max-width: 450px; }
        .alerta-exito { background-color: #155724; color: #d4edda; padding: 12px; border-radius: 5px; margin-top: 15px; text-align: center; font-weight: bold; }
        footer { text-align: center; color: #666; margin-top: 50px; }
    </style>
</head>
<body>
    <header style="display: flex; justify-content: space-between; align-items: center; padding: 20px 30px;">
        <h1 style="margin: 0; font-size: 2.5rem;">Panadería<span style="color: #e67e22;">San Juan</span></h1>
        <nav>
            <ul>
                <li><a id="enlace-inicio">Inicio / Servicios</a></li>
                <li><a id="enlace-productos">Productos</a></li>
                <li><a id="enlace-contacto">Contacto</a></li>
                {% if 'usuario' in session %}
                    <li><a href="/admin/dashboard" style="background-color: #28a745; padding: 8px 12px; border-radius: 4px;">Dashboard Admin</a></li>
                    <li><a href="/logout" style="background-color: #dc3545; padding: 8px 12px; border-radius: 4px;">Salir</a></li>
                {% else %}
                    <li><a id="enlace-admin" style="background-color: #4a3625; padding: 8px 12px; border-radius: 4px;">Admin Panel</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>
    
    <main>
        <div id="vista-inicio" class="seccion-contenido {% if vista_inicial and vista_inicial != 'inicio' %}oculto{% endif %}">
            <h2 style="color:#fff; margin-top: 25px;">Nuestros Servicios Especiales</h2>
            <section class="contenedor-tarjetas">
                {% for s in lista_servicios %}
                <article class="tarjeta">
                    <h2>{{ s.nombre }}</h2>
                    <p>{{ s.descripcion }}</p>
                    <span class="precio" style="font-size: 1rem;">Tarifa Base: S/. {{ "%.2f"|format(s.precio) }}</span>
                </article>
                {% endfor %}
            </section>
        </div>

        <div id="vista-productos" class="seccion-contenido {% if vista_inicial != 'productos' %}oculto{% endif %}">
            <h2 style="text-align:center;">Nuestro Catálogo de Productos</h2>
            <div class="contenedor-buscador">
                <input type="text" id="input-busqueda" class="input-buscador" placeholder="Buscar producto por nombre...">
            </div>

            <section class="catalogo-grid">
                {% for p in lista_productos %}
                <article class="producto-card" data-nombre="{{ p.nombre|lower }}">
                    <img src="{{ p.imagen }}" alt="{{ p.nombre }}">
                    <h3>{{ p.nombre }}</h3>
                    <p>{{ p.descripcion }}</p>
                    <span class="precio">S/. {{ "%.2f"|format(p.precio) }}</span>
                    <form action="/agregar_carrito" method="POST">
                        <input type="hidden" name="id" value="{{ p.id }}">
                        <input type="number" name="cantidad" value="1" min="1" style="width: 60px; text-align: center; margin-bottom: 10px;">
                        <button type="submit" class="btn-consultar">Añadir</button>
                    </form>
                </article>
                {% endfor %}
            </section>

            {% if 'historial' in session and session['historial'] %}
            <section class="contacto-simple" style="margin-top: 40px; border: 1px solid #28a745;">
                <h2><i class="fa-solid fa-cart-shopping"></i> Tu Carrito de Compras</h2>
                <table>
                    <thead><tr><th>Producto</th><th>Cantidad</th><th>Subtotal</th></tr></thead>
                    <tbody>
                        {% for item in session['historial'] %}
                        <tr><td>{{ item.nombre }}</td><td>{{ item.cantidad }}</td><td>S/. {{ "%.2f"|format(item.subtotal) }}</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div style="text-align: right; margin: 15px 0; font-size: 1.3rem; font-weight: bold; color: #28a745;">
                    Total: S/. {{ "%.2f"|format(session['historial']|sum(attribute='subtotal')) }}
                </div>

                <div style="background: #252525; padding: 20px; border-radius: 6px; margin-top: 20px;">
                    <h3><i class="fa-solid fa-user-check"></i> Completa tus Datos para Confirmar la Orden</h3>
                    <p style="color: #aaa; font-size: 0.9rem;">Al completar este paso, tus datos se guardarán de forma automática en el sistema de clientes de la panadería.</p>
                    <form action="/procesar_compra_cliente" method="POST">
                        <label>Tu Nombre y Apellido:</label>
                        <input type="text" name="cliente_nombre" required placeholder="Ej. Carlos Mendoza">
                        <label>Correo Electrónico:</label>
                        <input type="text" name="cliente_email" required placeholder="carlos@email.com">
                        <label>Teléfono Celular:</label>
                        <input type="text" name="cliente_telefono" required placeholder="912345678">
                        <input type="submit" value="Confirmar Pedido y Registrarme" style="background-color: #007bff;">
                    </form>
                </div>
            </section>
            {% endif %}

            {% if msg_exito %}<div class="alerta-exito">{{ msg_exito }}</div>{% endif %}
        </div>

        <div id="vista-admin" class="contenedor-admin-centrado {% if vista_inicial != 'admin' %}oculto{% endif %}">
            <div class="tarjeta-admin-medio">
                <h2 style="text-align:center;">Acceso Interno Administrativo</h2>
                {% if error %}<div class="alerta-error">{{ error }}</div>{% endif %}
                <form action="/login_verificar" method="POST">
                    <label>Usuario:</label>
                    <input type="text" name="usuario" required>
                    <label>Contraseña:</label>
                    <input type="password" name="clave" required>
                    <input type="submit" value="Ingresar al Sistema">
                </form>
            </div>
        </div>

        <section id="seccion-contacto-bloque" class="contacto-simple">
            <h2><i class="fa-solid fa-store"></i> Central de Contacto San Juan</h2>
            <div class="info-contacto">
                <div><i class="fa-solid fa-phone"></i><br><strong>Teléfono:</strong><br>+51 987 654 321</div>
                <div><i class="fa-solid fa-envelope"></i><br><strong>Correo:</strong><br>contacto@panaderiasanjuan.pe</div>
                <div><i class="fa-solid fa-location-dot"></i><br><strong>Ubicación:</strong><br>Av. Próceres de la Independencia, SJL</div>
            </div>
        </section>
    </main>
    
    <footer><p>© 2026 Panadería San Juan. Universidad Privada del Norte.</p></footer>

    <script>
        const enlaceInicio = document.getElementById('enlace-inicio');
        const enlaceProductos = document.getElementById('enlace-productos');
        const enlaceContacto = document.getElementById('enlace-contacto');
        const enlaceAdmin = document.getElementById('enlace-admin');
        const vistaInicio = document.getElementById('vista-inicio');
        const vistaProductos = document.getElementById('vista-productos');
        const vistaAdmin = document.getElementById('vista-admin');
        const bloqueContacto = document.getElementById('seccion-contacto-bloque');

        function ocultarVistas() {
            if(vistaInicio) vistaInicio.classList.add('oculto');
            if(vistaProductos) vistaProductos.classList.add('oculto');
            if(vistaAdmin) { vistaAdmin.classList.add('oculto'); vistaAdmin.style.setProperty('display', 'none', 'important'); }
        }
        if(enlaceInicio) { enlaceInicio.addEventListener('click', () => { ocultarVistas(); vistaInicio.classList.remove('oculto'); bloqueContacto.classList.remove('oculto'); }); }
        if(enlaceProductos) { enlaceProductos.addEventListener('click', () => { ocultarVistas(); vistaProductos.classList.remove('oculto'); bloqueContacto.classList.remove('oculto'); }); }
        if(enlaceContacto) { enlaceContacto.addEventListener('click', () => bloqueContacto.scrollIntoView({ behavior: 'smooth' })); }
        if(enlaceAdmin) { enlaceAdmin.addEventListener('click', () => { ocultarVistas(); bloqueContacto.classList.add('oculto'); vistaAdmin.classList.remove('oculto'); vistaAdmin.style.setProperty('display', 'flex', 'important'); }); }

        const inputBusqueda = document.getElementById('input-busqueda');
        if(inputBusqueda) {
            inputBusqueda.addEventListener('input', (e) => {
                const texto = e.target.value.toLowerCase();
                document.querySelectorAll('.producto-card').forEach(tarjeta => {
                    tarjeta.classList.toggle('oculto', !tarjeta.getAttribute('data-nombre').includes(texto));
                });
            });
        }
    </script>
</body>
</html>"""

# =========================================================================
# 3. DASHBOARD DEL ADMINISTRADOR CON OPCIÓN COMPLETA DE ELIMINAR (CRUD)
# =========================================================================
@app.route("/admin/dashboard")
def dashboard_admin():
    if 'usuario' not in session: return redirect(url_for('index', view='admin'))
    
    html_dashboard = """<!DOCTYPE html><html><head><meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; margin: 40px; }
        .box { background: #1e1e1e; padding: 25px; border-radius: 8px; max-width: 1100px; margin: 0 auto; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        h2 { color: #fff; border-bottom: 2px solid #634832; padding-bottom: 8px; margin-top: 30px;}
        .grid-formularios { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
        .tarjeta-form { background: #252525; padding: 20px; border-radius: 6px; flex: 1; min-width: 280px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; }
        th { background: #634832; color: white; padding: 10px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #2d2d2d; }
        label { font-weight: bold; display: block; margin-top: 10px; color: #ccc; }
        input[type="text"], input[type="number"], textarea { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #444; background-color: #1a1a1a; color: #fff; border-radius: 4px; box-sizing: border-box; }
        .btn-add { background-color: #28a745; color: white; border: none; padding: 10px; margin-top: 15px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; }
        .btn-danger { background: #dc3545; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 0.85rem; }
        .btn-back { background: #4a3625; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold; }
    </style>
    </head><body>
    <div class="box">
        <a href="/" class="btn-back"><i class="fa-solid fa-arrow-left"></i> Volver al Portal Principal</a>
        
        <h2 style="margin-top:20px;">Agregar Nuevo Contenido</h2>
        <div class="grid-formularios">
            <div class="tarjeta-form">
                <h3><i class="fa-solid fa-box"></i> Nuevo Producto</h3>
                <form action="/admin/productos/agregar" method="POST">
                    <label>Nombre:</label><input type="text" name="nombre" required>
                    <label>Descripción:</label><textarea name="descripcion" rows="1" required></textarea>
                    <label>Precio (S/.):</label><input type="number" step="0.01" name="precio" required>
                    <label>URL Imagen:</label><input type="text" name="imagen" value="https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=400">
                    <button type="submit" class="btn-add">Agregar Catálogo</button>
                </form>
            </div>
            <div class="tarjeta-form">
                <h3><i class="fa-solid fa-bell"></i> Nuevo Servicio</h3>
                <form action="/admin/servicios/agregar" method="POST">
                    <label>Nombre:</label><input type="text" name="nombre" required>
                    <label>Descripción:</label><textarea name="descripcion" rows="1" required></textarea>
                    <label>Precio Base (S/.):</label><input type="number" step="0.01" name="precio" required>
                    <button type="submit" class="btn-add">Agregar Servicio</button>
                </form>
            </div>
        </div>

        <h2><i class="fa-solid fa-bread-slice"></i> Gestión de Productos</h2>
        <table>
            <thead><tr><th>ID</th><th>Nombre</th><th>Precio</th><th>Acción</th></tr></thead>
            <tbody>
                {% for p in lista_p %}
                <tr><td>{{ p.id }}</td><td>{{ p.nombre }}</td><td>S/. {{ "%.2f"|format(p.precio) }}</td><td><a href="/admin/productos/eliminar/{{ p.id }}" class="btn-danger"><i class="fa-solid fa-trash"></i> Eliminar</a></td></tr>
                {% endfor %}
            </tbody>
        </table>

        <h2><i class="fa-solid fa-handshake"></i> Gestión de Servicios</h2>
        <table>
            <thead><tr><th>ID</th><th>Nombre</th><th>Precio Base</th><th>Acción</th></tr></thead>
            <tbody>
                {% for s in lista_s %}
                <tr><td>{{ s.id }}</td><td>{{ s.nombre }}</td><td>S/. {{ "%.2f"|format(s.precio) }}</td><td><a href="/admin/servicios/eliminar/{{ s.id }}" class="btn-danger"><i class="fa-solid fa-trash"></i> Eliminar</a></td></tr>
                {% endfor %}
            </tbody>
        </table>

        <h2><i class="fa-solid fa-users"></i> Tabla de Clientes Registrados Automáticamente</h2>
        <table>
            <thead><tr><th>ID</th><th>Nombre</th><th>Email</th><th>Teléfono</th><th>Acción</th></tr></thead>
            <tbody>
                {% for c in lista_c %}
                <tr><td>{{ c.id }}</td><td>{{ c.nombre }}</td><td>{{ c.email }}</td><td>{{ c.telefono }}</td><td><a href="/admin/clientes/eliminar/{{ c.id }}" class="btn-danger">Quitar Registro</a></td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    </body></html>"""
    return render_template_string(html_dashboard, lista_p=productos, lista_s=servicios, lista_c=clientes)

# =========================================================================
# 4. CONTROLADORES POST / ACCIONES Y REDIRECCIONES
# =========================================================================
@app.route("/")
def index():
    view = request.args.get('view', 'inicio')
    msg = request.args.get('msg', None)
    return render_template_string(HTML_PLANTILLA, lista_productos=productos, lista_servicios=servicios, vista_inicial=view, msg_exito=msg, error=None)

@app.route("/procesar_compra_cliente", methods=["POST"])
def procesar_compra_cliente():
    nombre = request.form.get("cliente_nombre")
    email = request.form.get("cliente_email")
    telefono = request.form.get("cliente_telefono")
    
    existe = any(c['email'].lower() == email.lower() for c in clientes)
    if not existe:
        nuevo_id = max([c['id'] for c in clientes]) + 1 if clientes else 1
        clientes.append({"id": nuevo_id, "nombre": nombre, "email": email, "telefono": telefono})
    
    session.pop('historial', None)
    return redirect(url_for('index', view='productos', msg=f"Gracias por tu pedido, {nombre}. Tu registro se completó automáticamente."))

@app.route("/admin/productos/eliminar/<int:id>")
def eliminar_producto_admin(id):
    if 'usuario' not in session: return redirect(url_for('index'))
    global productos
    productos = [p for p in productos if p['id'] != id]
    return redirect(url_for('dashboard_admin'))

@app.route("/admin/servicios/eliminar/<int:id>")
def eliminar_servicio_admin(id):
    if 'usuario' not in session: return redirect(url_for('index'))
    global servicios
    servicios = [s for s in servicios if s['id'] != id]
    return redirect(url_for('dashboard_admin'))

@app.route("/admin/clientes/eliminar/<int:id>")
def eliminar_cliente(id):
    if 'usuario' not in session: return redirect(url_for('index'))
    global clientes
    clientes = [c for c in clientes if c['id'] != id]
    return redirect(url_for('dashboard_admin'))

@app.route("/admin/productos/agregar", methods=["POST"])
def agregar_producto_admin():
    if 'usuario' not in session: return redirect(url_for('index'))
    nuevo_id = max([p['id'] for p in productos]) + 1 if productos else 1
    productos.append({
        "id": nuevo_id, "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"), "precio": float(request.form.get("precio")),
        "imagen": request.form.get("imagen")
    })
    return redirect(url_for('dashboard_admin'))

@app.route("/admin/servicios/agregar", methods=["POST"])
def agregar_servicio_admin():
    if 'usuario' not in session: return redirect(url_for('index'))
    nuevo_id = max([s['id'] for s in servicios]) + 1 if servicios else 1
    servicios.append({
        "id": nuevo_id, "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"), "precio": float(request.form.get("precio"))
    })
    return redirect(url_for('dashboard_admin'))

@app.route("/agregar_carrito", methods=["POST"])
def agregar_carrito():
    p_id = int(request.form.get("id"))
    cantidad = int(request.form.get("cantidad"))
    seleccionado = next((p for p in productos if p['id'] == p_id), None)
    if seleccionado:
        if 'historial' not in session: session['historial'] = []
        session['historial'].append({
            "nombre": seleccionado['nombre'], "cantidad": cantidad, "subtotal": seleccionado['precio'] * cantidad
        })
        session.modified = True
    return redirect(url_for('index', view='productos'))

@app.route("/login_verificar", methods=["POST"])
def login_verificar():
    if request.form.get("usuario") == ADMIN_USER and request.form.get("clave") == ADMIN_PASS:
        session['usuario'] = ADMIN_USER
        return redirect(url_for('dashboard_admin'))
    return render_template_string(HTML_PLANTILLA, lista_productos=productos, lista_servicios=servicios, vista_inicial='admin', error="Usuario o clave incorrectos.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index', view='inicio'))

# =========================================================================
# 5. CONFIGURACIÓN COMPROBADA ANTI-BLOQUEOS
# =========================================================================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False, threaded=True)

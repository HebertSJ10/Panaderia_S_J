from flask import Flask, render_template_string, request, session

app = Flask(__name__)
# Clave de seguridad para habilitar el uso de sesiones y guardar el historial
app.secret_key = 'panaderia_historial_'

# 1. Definición del contenido HTML Principal (Catálogo)
pagina_html = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Panadería San Juan</title>
  <style>
    body { font-family: sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; }
    header { background-color: #634832; color: white; padding: 20px; text-align: center; }
    nav { background: #333; padding: 10px; text-align: center; }
    nav a { color: white; margin: 0 15px; text-decoration: none; font-size: 14px; font-weight: bold; }
    .contenido { max-width: 1100px; margin: 20px auto; padding: 20px; }
    .contenedor-productos { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
    .producto { 
      background: white; border: 1px solid #ddd; width: 220px; 
      padding: 0; border-radius: 8px; text-align: center;
      overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .producto img { width: 100%; height: 150px; object-fit: cover; }
    .info { padding: 15px; }
    .producto h3 { margin: 10px 0; color: #634832; font-size: 18px; }
    .producto p { font-size: 13px; color: #666; margin-bottom: 10px; }
    .precio { font-weight: bold; color: #d35400; font-size: 16px; display: block; margin-bottom: 10px; }
    .controles { margin-top: 10px; padding-top: 10px; border-top: 1px dashed #eee; }
    .btn-agregar { 
        background-color: #27ae60; color: white; border: none; 
        padding: 8px 12px; border-radius: 4px; cursor: pointer; font-weight: bold;
    }
    .btn-agregar:hover { background-color: #219150; }
    input[type="number"] { width: 45px; padding: 5px; margin-right: 5px; border: 1px solid #ccc; border-radius: 4px; }
    footer { text-align: center; padding: 20px; font-size: 12px; color: #888; margin-top: 40px; }
  </style>
</head>
<body>
  <nav>
    <a href="/">INICIO</a>
    <a href="#">PRODUCTOS</a>
    <a href="#">CONTACTO</a>
  </nav>
  <header>
    <h1>PANADERÍA SAN JUAN</h1>
    <p>Catálogo Visual de Productos</p>
  </header>
  <div class="contenido">
    <div class="contenedor-productos">
      
      <div class="producto">
        <img src="https://images.unsplash.com/photo-1586444248902-2f64eddc13df?q=80&w=400" alt="Pan Frances">
        <div class="info">
          <h3>Pan Francés</h3>
          <p>Tradicional y crujiente.</p>
          <span class="precio">S/ 0.20 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Pan Francés">
            <input type="hidden" name="precio" value="0.20">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div> 
      </div>

      <div class="producto">
        <img src="https://www.atavolaregaz.it/es/recetas/pan-ciabatta/images/16x9/image_r100.jpg" alt="Chabata">
        <div class="info">
          <h3>Chabata</h3>
          <p>Pan artesanal rústico.</p>
          <span class="precio">S/ 0.30 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Chabata">
            <input type="hidden" name="precio" value="0.30">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

      <div class="producto">
        <img src="https://images.unsplash.com/photo-1598373182133-52452f7691ef?q=80&w=400" alt="Pan de molde">
        <div class="info">
          <h3>Pan de Molde</h3>
          <p>Suave y para sándwich.</p>
          <span class="precio">S/ 7.50 x paquete</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Pan de Molde">
            <input type="hidden" name="precio" value="7.50">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

      <div class="producto">
        <img src="https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=400" alt="Torta Chocolate">
        <div class="info">
          <h3>Torta de Chocolate</h3>
          <p>Cacao puro nacional.</p>
          <span class="precio">S/ 40.00 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Torta de Chocolate">
            <input type="hidden" name="precio" value="40.00">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

      <div class="producto">
        <img src="https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=400" alt="Cachito">
        <div class="info">
          <h3>Cachito Mantequilla</h3>
          <p>Suave y tradicional.</p>
          <span class="precio">S/ 0.50 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Cachito de Mantequilla">
            <input type="hidden" name="precio" value="0.50">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

      <div class="producto">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9SwWuaLPjSZbZR5ouyneVKiCxXvpfymLuEw&s" alt="Baguette">
        <div class="info">
          <h3>Pan Baguette</h3>
          <p>Largo y muy crocante.</p>
          <span class="precio">S/ 3.00 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Pan Baguette">
            <input type="hidden" name="precio" value="2.00">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

      <div class="producto">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3AL1iExIyFoi3WvX3n6UzihA6QNU9aY5bUg&s" alt="Empanada">
        <div class="info">
          <h3>Empanada Carne</h3>
          <p>Relleno clásico criollo.</p>
          <span class="precio">S/ 5.00 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Empanada de Carne">
            <input type="hidden" name="precio" value="5.00">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

      <div class="producto">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpJwuvsuCh-r63wUnZBMlU4Twbft-DMqZ1bg&s" alt="Torta Helada"> 
        <div class="info">
          <h3>Torta Helada</h3>
          <p>Bizcocho con gelatina.</p>
          <span class="precio">S/ 30.00 x unidad</span>
          <form action="/pedido" method="POST" class="controles">
            <input type="hidden" name="producto" value="Torta Helada">
            <input type="hidden" name="precio" value="30.00">
            <input type="number" name="cantidad" value="1" min="1">
            <button type="submit" class="btn-agregar">Añadir</button>
          </form>
        </div>
      </div>

    </div>
  </div>
  <footer>
    <p>Universidad Privada del Norte | Fundamentos de programación</p>
  </footer>
</body>
</html>
"""

# 2. Definición del contenido HTML para el Historial (Mismos colores)
historial_html = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Mi Pedido - Panadería San Juan</title>
  <style>
    body { font-family: sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; }
    header { background-color: #634832; color: white; padding: 20px; text-align: center; }
    .contenido { max-width: 650px; margin: 40px auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h2 { color: #634832; border-bottom: 2px solid #634832; padding-bottom: 10px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th { text-align: left; background: #eee; padding: 10px; color: #634832; }
    td { padding: 10px; border-bottom: 1px solid #eee; }
    .total-seccion { text-align: right; margin-top: 20px; font-size: 1.3em; font-weight: bold; color: #d35400; }
    .btn-zona { display: flex; justify-content: space-between; margin-top: 30px; }
    .btn-volver { padding: 10px 20px; background-color: #333; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; }
    .btn-listo { padding: 10px 20px; background-color: #27ae60; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
    .btn-volver:hover { background-color: #555; }
    .btn-listo:hover { background-color: #219150; }
    footer { text-align: center; padding: 20px; font-size: 12px; color: #888; }
  </style>
</head>
<body>
  <header>
    <h1>PANADERÍA SAN JUAN</h1>
  </header>
  <div class="contenido">
    <h2>Pedido Confirmado</h2>
    <p>Has agregado satisfactoriamente: <b>{{ ultima_cantidad }} x {{ ultimo_producto }}</b></p>
    
    <h3>Resumen actual de la compra:</h3>
    <table>
      <thead>
        <tr>
          <th>Producto</th>
          <th>Cant.</th>
          <th>Subtotal</th>
        </tr>
      </thead>
      <tbody>
        {% for item in historial %}
        <tr>
          <td>{{ item.nombre }}</td>
          <td>{{ item.cantidad }}</td>
          <td>S/ {{ "%.2f"|format(item.subtotal) }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>

    <div class="total-seccion">
      Total acumulado: S/ {{ "%.2f"|format(total_final) }}
    </div>
    
    <div class="btn-zona">
      <a href="/" class="btn-volver">VOLVER AL CATÁLOGO</a>
      <button class="btn-listo" onclick="alert('¡Gracias por su compra! El pedido ha sido procesado.')">LISTO</button>
    </div>
  </div>
  <footer>
    <p>Universidad Privada del Norte | Fundamentos de programación</p>
  </footer>
</body>
</html>
"""

@app.route("/")
def index():
    """ Muestra la interfaz principal con todos los productos disponibles """
    return render_template_string(pagina_html)

@app.route("/pedido", methods=["POST"])
def pedido():
    """ Recibe los datos del formulario, gestiona la sesión del historial y calcula montos """
    nombre = request.form.get("producto")
    cantidad = int(request.form.get("cantidad"))
    precio = float(request.form.get("precio"))
    
    # Si no existe la lista de historial en la sesión, la creamos
    if 'historial' not in session:
        session['historial'] = []
    
    # Calculamos el costo por esta selección de producto
    subtotal_item = cantidad * precio
    
    # Creamos el registro del item y lo añadimos a la lista de la sesión
    item_pedido = {
        "nombre": nombre, 
        "cantidad": cantidad, 
        "subtotal": subtotal_item
    }
    
    # Actualización segura de la sesión en Flask
    lista_temp = session['historial']
    lista_temp.append(item_pedido)
    session['historial'] = lista_temp
    
    # Calculamos el total de toda la lista acumulada
    total_acumulado = sum(item['subtotal'] for item in session['historial'])
    
    return render_template_string(
        historial_html, 
        ultimo_producto=nombre, 
        ultima_cantidad=cantidad,
        historial=session['historial'],
        total_final=total_acumulado
    )

if __name__ == "__main__":
    # Inicializa la aplicación en modo local
    app.run(host="127.0.0.1", port=8080, debug=False)

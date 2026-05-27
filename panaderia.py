from flask import Flask, render_template_string

app = Flask(__name__)

# 1. Definición del contenido HTML
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
    .contenido { max-width: 1000px; margin: 20px auto; padding: 20px; }
    .contenedor-productos { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
    .producto { 
      background: white; 
      border: 1px solid #ddd; 
      width: 220px; 
      padding: 0; 
      border-radius: 8px; 
      text-align: center;
      overflow: hidden; 
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .producto img { width: 100%; height: 150px; object-fit: cover; }
    .info { padding: 15px; }
    .producto h3 { margin: 10px 0; color: #634832; font-size: 18px; }
    .producto p { font-size: 13px; color: #666; margin-bottom: 10px; }
    .precio { font-weight: bold; color: #d35400; font-size: 16px; }
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
          <span class="precio">S/ 0.20 x pan</span>
        </div> 
      </div>
      <div class="producto">
        <img src="https://www.atavolaregaz.it/es/recetas/pan-ciabatta/images/16x9/image_r100.jpg" alt="Chabata">
        <div class="info">
          <h3>Chabata</h3>
          <p>Pan artesanal de corteza rústica.</p>
          <span class="precio">S/ 0.20 x pan</span>
        </div>
      </div>
      <div class="producto">
        <img src="https://images.unsplash.com/photo-1598373182133-52452f7691ef?q=80&w=400" alt="Pan de molde">
        <div class="info">
          <h3>Pan de Molde</h3>
          <p>Suave y para sándwich.</p>
          <span class="precio">S/ 6.50 x paquete</span>
        </div>
      </div>
      <div class="producto">
        <img src="https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=400" alt="Torta">
        <div class="info">
          <h3>Torta de Chocolate</h3>
          <p>Cacao puro nacional.</p>
          <span class="precio">S/ 40.00</span>
        </div>
      </div>
      <div class="producto">
        <img src="https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=400" alt="Cachito">
        <div class="info">
          <h3>Cachito de mantequilla</h3>
          <p>Suave, tradicional y saladito.</p>
          <span class="precio">S/ 0.20 x pan</span>
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

@app.route("/")
def index():
    return render_template_string(pagina_html)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)

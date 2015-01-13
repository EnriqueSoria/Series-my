# Series-my
Series-my: enlaces de series a tu propio ordenador.

## Descripción
Organiza tus series gracias a la información que se puede descargar de series.ly en una página web local.

Escanea una serie de directorios en busca de series y crea un HTML estático a partir de los ficheros info.json de cada serie, y con tus propios capítulos crea una web de enlaces a tu propio ordenador.

Obviamente esto no funciona de un ordenador a otro, ya que el contenido no está almacenado de ningún modo en la web, sino que te muestra la ruta a tu disco duro.

### How-to
Por defecto, todos los navegadores impiden abrir enlaces a tu ordenador, para evitar esto, instala [esta extensión](https://github.com/EnriqueSoria/firefox_addon_local_filesystem_links) de Firefox.

También hace falta Bootstrap, que se puede enlazar:
```html
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	<!-- Optional theme -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css">
	<!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
```

Para esconder/mostrar un `div` se usa Bootstrap, y no funciona si ves la página web desde `file:///<path>/index.html`, de modo que no podrás usarla si no la ves desde un servidor.

Puedes hacer un servidor http con este script (ejecútalo en la misma carpeta que `index.html`:
```python
import SimpleHTTPServer
import SocketServer

# Puerto que quieras (normalmente 80 o >=8000)
PORT = 8000

# Creamos el servidor
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
```
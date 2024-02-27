import requests
from bs4 import BeautifulSoup
import time
import os


# Variable del producto a buscar
busqueda = input("Busqueda: ")
# URL con variable dentro 
url = f"https://listado.mercadolibre.com.ar/{busqueda}"

# Pido al servidor de la URL que me pase la página como si fuera un usuario normal
response = requests.get(url)

# Variable con el contenido de la página
buscar = BeautifulSoup(response.content, "html.parser")

# Extraigo el ol que contiene los productos
orderList = buscar.find("ol", class_="ui-search-layout ui-search-layout--stack shops__layout")

# Busca el link del producto
linkProducto = orderList.find("a", class_="ui-search-item__group__element shops__items-group-details ui-search-link")['href']

# Entra al link
response = requests.get(linkProducto)
buscar = BeautifulSoup(response.content,"html.parser")

# Busca el link de más vendidos
linkMasVendidos = None  # Inicializar con None
while not linkMasVendidos:
    linkMasVendidos = buscar.find("a", class_="ui-pdp-promotions-pill-label__target")
    if not linkMasVendidos:
        # Intenta nuevamente después de un breve tiempo de espera
        time.sleep(1)
        response = requests.get(linkProducto)
        buscar = BeautifulSoup(response.content, "html.parser")

linkMasVendidos = linkMasVendidos['href']
response = requests.get(linkMasVendidos)
buscar = BeautifulSoup(response.content, "html.parser")
masVendidoEn = buscar.find("h2", class_="ui-search-breadcrumb__title shops-custom-primary-font")

# Busca el div contenedor de los demás divs
divContenedor = buscar.find("div", class_="ui-search-layout--grid__grid")

# Obtiene datos
nombrePR = divContenedor.findAll("p", class_="ui-recommendations-card__title")
linkPR = [div.find("a")["href"] for div in divContenedor.findAll("div", class_="ui-recommendations-card")]
precioPR = divContenedor.findAll("span", class_="andes-visually-hidden")
imagenPR = divContenedor.findAll("img", class_="ui-recommendations-card__image")

a = 0

for nombre, precio in zip(nombrePR, precioPR):
    a += 1
    print(a)
    print(nombre.get_text(strip=True))  # Se utiliza get_text() para obtener solo el texto sin etiquetas HTML
    print(precio.get_text(strip=True))  # Se utiliza get_text() para obtener solo el texto sin etiquetas HTML
    print()


#EN ESTA PARTE DE CODIGO ESTOY HACIENDO UN HTML CON LOS DATOS


# Crear el archivo index.html
with open('index.html', 'w') as file:
    # Escribir el encabezado HTML
    file.write('<html>\n')
    file.write('<style>li { list-style-type: none; }</style>\n')
    file.write('<body>\n')

    # Escribir la lista ordenada (ol)
    file.write('<ol>\n')

    # Escribir los elementos de la lista
    for nombre, precio, imagen in zip(nombrePR, precioPR, imagenPR):
        file.write('<li>{}</li>\n'.format(nombre.get_text(strip=True)))
        file.write('<li>{}</li>\n'.format(precio.get_text(strip=True)))
        file.write('<li><img src="{}"></li>\n'.format(imagen['src']))

    # Cerrar la lista ordenada (ol)
    file.write('</ol>\n')

    # Cerrar el cuerpo y el HTML
    file.write('</body>\n')
    file.write('</html>\n')

# Libreria para pedir paginas a servidores
import requests

# Libreria para leer HTML y XML
from bs4 import BeautifulSoup

# Extrae todos los cines de una ciudad dado su id de cinemex, ver scrapUnaPagina.py
def extraeCinesCiudad(ident): 
    # Pide la pagina a cinemex, del estado ident, sustituye en {}
    paginaCruda = requests.get("https://cinemex.com/cines/{}".format(ident))
    # Interpreta el HTML de la pagina
    paginaProcesada = BeautifulSoup(paginaCruda.text, "html.parser")
    # Aislamos el elemento que contiene los datos de interes
    cuadro = paginaProcesada.find("ul", attrs={"class":"collapsable-list"})
    # Sabemos que cada dato esta en un li con clase cinema-item
    lista = cuadro.findAll("li", attrs={"class":"cinema-item"})
    # Para cada elemento aisla los datos
    datos = []
    for ele in lista:
        # La direccion esta en un atributo data-adress
        direccion = ele.get_attribute_list("data-address")[0]
        # El nombre esta en el texto del tag "a" del elemento de la lista
        nombre = ele.find("a").getText().lstrip().rstrip()
        # La id esta en un atributo data-adress
        ident = ele.get_attribute_list("id")[0]
        # El url del cine esta en el atributo href del tag "a"
        url = ele.find("a").get_attribute_list("href")[0]
        # Se guardan resultados en la lista de datos
        datos.append((ident,nombre,direccion,url))
    return datos





# Pide la pagina a cinemex
paginaCruda = requests.get("https://cinemex.com/cines")

# Interpreta el HTML de la pagina
paginaProcesada = BeautifulSoup(paginaCruda.text, "html.parser")

# Aislamos el elemento que contiene los estados
cuadro = paginaProcesada.find(attrs={"id":"cinemas-select-city"})
ciudades = cuadro.findAll("option")

# Sacamos el identificador y el nombre
datosCiudad = []
datosCines = []
for ele in ciudades[0:4]:
    ident = ele.get_attribute_list("value")[0]
    nombre = ele.getText().lstrip().rstrip()
    print(nombre)
    datosCiudad.append((ident,nombre))
    cines = extraeCinesCiudad(ident)
    datosCines.extend(cines)

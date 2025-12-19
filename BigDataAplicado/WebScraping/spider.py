#!/usr/bin/env python3

import os
from re import S
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import smtplib as smtplib
from email.mime.text import MIMEText # Sirve para escribir el asunto y curpo del correo en texto plano antes de enviarlo con el smtp
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Funcion para enviar correo electrónico
def enviar_correo(mng_error,email_body,email_subject):
    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Credenciales
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    load_dotenv(dotenv_path)
    remitente = "mayosalem@gmail.com"
    password = os.getenv("OUTLOOK_PASS")

    # Crear mensaje
    destinatario = "marsolcha@alu.edu.gva.es"
    asunto = email_subject
    cuerpo = email_body

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain"))

    try:
        # Conexión al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Habilitar TLS
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        mng_info("Correo enviado correctamente!")
    except Exception as e:
        mng_error(f"No se pudo enviar el correo electrónico a {destinatario}. Error: {e}")


# Funciones de logg
def log_message(message, type="info"):
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  log_dir = os.path.join(BASE_DIR, "samples")
  log_file = os.path.join(log_dir, "scraping_log_.txt")

  # Asegurar que la carpeta existe
  os.makedirs(log_dir, exist_ok=True)

  # Escribir log
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(log_file, "a") as f:
    f.write(f"{timestamp} [{type.upper()}] {message}\n")
  print(f"[{type.upper()}] {message}")

def mng_info(text_info):
    log_message(text_info, "info")

def mng_error(text_error):
    log_message(text_error, "error")

# Función para comprobar la URL y obtener el contenido
def checkUrl(url):
  page = requests.get(url, headers=cabeceras)
  if page.status_code != 200:
    mng_error(f'Error en la petición {url}: {page.status_code}')
    return None
  mng_info(f'Petición exitosa para {url}')
  return bs(page.content, 'lxml')

# Función para formatear el precio
def formatPrice(price):
  valor = price.replace(',',".")
  valor = valor.split('\xa0')[0]
  return valor

# Función para obtener la moneda
def get_moneda(price):
    parts = price.split('\xa0')
    if len(parts) > 1:
        return parts[1]
    return 'N/A'

# Función para escribir los datos en un CSV
def escribir_csv(products_data):
  # Base path donde está el script
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  samples_dir = os.path.join(BASE_DIR, "samples")

  # Crear la carpeta si no existe
  os.makedirs(samples_dir, exist_ok=True)

  # Crear ruta completa del CSV
  csv_filename = os.path.join(samples_dir, f'{datetime.now().strftime("%Y-%m-%d")}-[druni|MariaSolaz].csv')

  # Guardar CSV
  products_df = pd.DataFrame(products_data)
  products_df.to_csv(csv_filename, index=False)

  mng_info(f"Datos de productos guardados en {csv_filename}")

# Función para obtener productos de una categoría
def getProductsFromCategory(url, category_name):
  listaArticulos = []
  soup = checkUrl(url)
  if soup is None:
      return listaArticulos
  list_items = soup.find_all('li', class_='item product product-item')

  if list_items:
    for item in list_items:
      product = item.find('div', class_='product-item-info')
      product_id = item.find('input', attrs={'name':'product','value': True})

      if product_id:
        product_id = product_id.get('value')
      else:
        product_id = 'N/A'


      if product:
        
        # Nombre
        name_tag = product.find('a', class_='product-item-link')
        name = name_tag.text.strip() if name_tag else 'N/A'

        # Descripcion
        description_tag = product.find('span', class_='product description product-item-description')
        description = description_tag.text.strip() if description_tag else 'N/A'

        # Precio y divisa
        price_tag = product.find('span', class_='price')
        price = formatPrice(price_tag.text.strip()) if price_tag else 'N/A'
        divisa = get_moneda(price_tag.text.strip()) if price_tag else 'N/A'

        # Precio viejo
        old_price_tag = product.find('span', class_='old-price')
        old_price = formatPrice(old_price_tag.text.strip()) if old_price_tag else 'N/A'
        if old_price == price:
            old_price = 'N/A'

        # Imagen
        img_tag = product.find('img', class_='product-image-photo')
        img = img_tag['src'] if img_tag else 'N/A'

        # URL
        url_tag = product.find('a', class_='product-item-link')
        url = url_tag['href'] if url_tag else 'N/A'

        articulo = {
            'categoria': category_name,
            'product_id': product_id,
            'name': name,
            'description': description,
            'price': price,
            'old_price': old_price,
            'divisa': divisa,
            'img': img,
            'url': url
        }

        listaArticulos.append(articulo)

      else:
        mng_info(f"No se encontró información del producto dentro de este elemento de la lista (ID: {product_id}).")
  else:
    mng_info("No se encontraron elementos de la lista de productos en esta página.")
  return listaArticulos

cabeceras = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rb:109.0) Gecko/20100101 Firefox/117.0'}
url = 'https://www.druni.es/solares/proteccion-solar'
soup = checkUrl(url)

# Recorrer las categorías
try:
    categoriaPadre = soup.find_all('li', class_='item current active has-childs')
    if not categoriaPadre:
        mng_error("No se encontraron categorías principales.")
        email_body = "El scraping no se pudo completar porque no se encontraron categorías principales."
        email_subject = "Error en el Scraping de Druni"
    else:
        nombreCategoriaPadre = soup.find('li', class_='item current active has-childs').find('a').text.strip()
        listaDatosArticulos = []
        for categoria in categoriaPadre:
          for tipo in categoria.find_all('li', class_='item'):
            nombre = tipo.find('a').text.strip()
            url = tipo.find('a')['href']
            mng_info(f"Scraping de la categoría: {nombre}")
            listaDatosArticulos.extend(getProductsFromCategory(url, nombre))

        escribir_csv(listaDatosArticulos)
        email_body = f"El scraping de Druni se completó exitosamente. Se guardaron {len(listaDatosArticulos)} artículos en el archivo CSV."
        email_subject = "Scraping de Druni Completado"

except Exception as e:
    mng_error(f"Ocurrió un error durante el scraping: {e}")
    email_body = f"Ocurrió un error durante el scraping de Druni: {e}"
    email_subject = "Error en el Scraping de Druni"

finally:
    enviar_correo(mng_error,email_body,email_subject)
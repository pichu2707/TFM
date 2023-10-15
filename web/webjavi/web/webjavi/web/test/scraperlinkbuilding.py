from os import name
import os
import sys
import time
from datetime import datetime, timedelta, timezone
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

"""Creamos una conexión con el drive de Chrome a internet, teniendo en cuenta los diferentes sistemas operativos y 
tipos de pantallas """

def crear_driver_chrome(headless=True):
    # for windows
    if name == 'nt':
        PATH = Service(executable_path='chromedriver.exe')

    # for mac and linux(here, os.name is 'posix')
    else:
        PATH = Service(executable_path='chromedriver.exe')

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    options.add_argument('--lang=es')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'es,es_ES'})
    
    driver = webdriver.Chrome(service=PATH, options=options)

    driver.set_window_size(1920, 1080)
    driver.maximize_window()

    return driver

# Tomamos los datos del json config
def get_config():
    with open('/home/javier/Documentos/TFM/web/webjavi/scraper/config.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        escanerConfig = dict(data)
    return escanerConfig

#Función que hace clic según el selector que funcione con JavaScript que marquemos
def click_element_by_tipo_selector(driver, wait, tipoSelector, textoSelector):
    try:
        elemento = wait.until(EC.presence_of_element_located((tipoSelector, textoSelector)))
        driver.execute_script("arguments[0].click();", elemento)
    except Exception as e:
        pass

#Clic en elementor sin JS que seleccionemos
def click_element_sin_js_by_tipo_selector(driver, wait, tipoSelector, textoSelector):
    try:
        elemento = wait.until(EC.presence_of_element_located((tipoSelector, textoSelector)))
        elemento.click()
    except Exception as e:
        pass

#Escribiremos un texto en el elemento selccionado por JS
def escribir_text_en_element_by_tipo_selector(driver, wait, tipoSelector, textoSelector, textoAEscribir):
    try:
        elemento = wait.until(EC.presence_of_element_located((tipoSelector, textoSelector)))
        elemento.send_keys(textoAEscribir)
    except Exception as e:
        pass

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
from webdriver_manager.chrome import ChromeDriverManager

"""Creamos una conexión con el drive de Chrome a internet, teniendo en cuenta los diferentes sistemas operativos y 
tipos de pantallas """

def crear_driver_chrome(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    options.add_argument('--lang=es')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'es,es_ES'})

    # Uso de Service() con ChromeDriverManager

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)

    driver.set_window_size(1920, 1080)
    driver.maximize_window()

    return driver

# Tomamos los datos del json config
def get_config():
    with open('/home/javier/Documentos/TFM/web/webjavi/config.json', encoding='utf-8') as json_file:
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

# Toma los medios desde las peticiones JQuery
def js_function_get_medios_prensarank():
    return """
        let medios = []; 
        $('#listTable').DataTable().rows().data().each(function(medio){
            medios.push(medio);
            });
        return medios;
    """

#Toma las ID de los medios por JQuery
def js_function_get_medios_ids_prensarank():
    return """
        let mediosIds = []; 
        $('#listTable').DataTable().rows().data().each(function(medio){
            mediosIds.push(medio['id']);
            });
        return mediosIds;
    """

#Función de selección de opciones
def select_change_option(agrupacionSelector, texto, estado):
    return '$(\'select#' + agrupacionSelector + ' option:contains("' + texto + '")\').prop(\'selected\', ' + estado + ').change();'

#Toma la estructura de las tablas
def get_estructura_ths_thead(tr):
    datos = []
    ths = tr.find_elements(By.TAG_NAME, 'th')
    for td in ths:
        datos.append(td.text)

    return datos

#Comprueba que no ha habido cambios en la estructura
def comprobar_estructora_sin_cambios(estructura):
    estructuraSinCambios = False
    if(estructura == ['NOMBRE', 'PAÍS', 'DR', 'DA', 'CF', 'TF', 'OBL', 'RD', 'TRÁFICO', 'PRECIO', '']):
        estructuraSinCambios = True

    return estructuraSinCambios

#Toma la cabecera de las tablas
def get_estructura_ths_thead_arr_pos_cabeceras(tr):
    arrPosCabeceras = {}
    contador = 0
    tds = tr.find_elements(By.TAG_NAME, 'th')
    for td in tds:
        arrPosCabeceras[td.text] = contador
        contador += 1

    return arrPosCabeceras

#Toma la tabla de Prensarank
def get_table_data_prensarank(driver, wait):
    try:
        dataFinal = []

        # Comprobar que la tabla tenga la mimsa estructura
        trHead = driver.find_element(By.XPATH, "//table[@id='listTable']/thead//tr")

        estructura = get_estructura_ths_thead(trHead)

        if(comprobar_estructora_sin_cambios(estructura)):
            arrPosCabeceras = get_estructura_ths_thead_arr_pos_cabeceras(trHead)

            btnSiguiente = driver.find_element(By.XPATH, '//li[ contains(@class, "paginate_button page-item next") ]')
            
            while(btnSiguiente.get_attribute('class').find('disabled') == -1):
                dataFinal += driver.execute_script(js_function_get_medios_prensarank())
                
                # Click en Siguiente Página
                driver.execute_script("arguments[0].click();", btnSiguiente)
                time.sleep(1)
                
                btnSiguiente = driver.find_element(By.XPATH, '//li[ contains(@class, "paginate_button page-item next") ]')
                time.sleep(3)
            # Recoger Datos de la última página
            dataFinal += driver.execute_script(js_function_get_medios_prensarank())
        return dataFinal
    
    except:
        pass

def get_table_data_ids_prensarank(driver, wait):
        try:
            dataFinal = []

            # Comprobar que la tabla tenga la mimsa estructura
            trHead = driver.find_element(By.XPATH, "//table[@id='listTable']/thead//tr")
            estructura = get_estructura_ths_thead(trHead)

            if(comprobar_estructora_sin_cambios(estructura)):
                arrPosCabeceras = get_estructura_ths_thead_arr_pos_cabeceras(trHead)

                btnSiguiente = driver.find_element(By.XPATH, '//li[ contains(@class, "paginate_button page-item next") ]')
                while( btnSiguiente.get_attribute('class').find('disabled') == -1):

                    dataFinal += driver.execute_script(js_function_get_medios_ids_prensarank())

                    # Click en Siguiente Página
                    driver.execute_script("arguments[0].click();", btnSiguiente)
                    time.sleep(1)

                    btnSiguiente = driver.find_element(By.XPATH, '//li[ contains(@class, "paginate_button page-item next") ]')
                
                # Recoger Datos de la última página
                dataFinal += driver.execute_script(js_function_get_medios_ids_prensarank())
            
            return dataFinal
        except:
            pass

#Toma las opciones seleccionadas
def js_function_get_select_options(selector, valOText):
    js = 'let options = [];'
    js += '$("' + selector + '").each(function(){'
    js += 'options.push($(this).'+ valOText +'().trim());'
    js += '});return options;'

    return js
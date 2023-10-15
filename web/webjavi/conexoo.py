import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webjavi.settings.local')

django.setup()

from applications.scraperconexoo.models import scraperConexoo
from selenium.webdriver.common.by import By
import time
from datetime import datetime,timezone
from os import name
from selenium.webdriver.support.wait import WebDriverWait


import os
from scraperlinkbuilding import *

def obtener_datos():
    escanerConfig = get_config()
    driver = crear_driver_chrome(True)
    wait = WebDriverWait(driver, escanerConfig['timeoutSeconds'])
    time.sleep(1)

    #Accediendo a Conexoo

    print('abriendo Conexoo')
    driver.get(escanerConfig['conexookUrl'])
    driver.implicitly_wait(escanerConfig['timeoutSeconds'])
    time.sleep(1)

    #Accediendo al area de cliente

    print("Entrando en conexoo")
    click_element_by_link_text(driver,wait,By.LINK_TEXT, 'Acceso Clientes')
    time.sleep(1)
    print('paso privacidad')
    time.sleep(2)
    print('entra en acceso a clientes')
    time.sleep(3)

    #Introduciendo credenciales
    escribir_text_en_element_by_tipo_selector(driver,wait,By.ID,'login',escanerConfig['conexookUser'])
    time.sleep(1.5)
    escribir_text_en_element_by_tipo_selector(driver,wait, By.ID, 'password', escanerConfig['conexookPass'])
    time.sleep(3)
    # par = driver.current_url
    # rellenar_resultado_recaptcha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
    # )
    print('clic de recapchat')
    # click_element_by_tipo_selector(driver,wait,By.CLASS_NAME, 'g-recaptcha')
    clicar = driver.find_element(By.CLASS_NAME, 'g-recaptcha')
    clicar.click()
    time.sleep(5)
    click_element_by_tipo_selector(driver,wait, By.CLASS_NAME, 'btn-lg')
    time.sleep(4)
    click_element_by_tipo_selector(driver,wait,By.XPATH,'//span[normalize-space()="Comprar artículos"])')
    time.sleep(2)


    tipoMedios = ['Webs y Blogs', 'Periódicos']
    dataFinalArr = {}
    time.sleep(2)

    #Empezamos a extraer datos
    for tipoMedio in tipoMedios:
    #Clics en webs y Blogs/Periodicos
        driver.execute_script("$('ul#sidebarnav a:contains(\"" + tipoMedio + "\")')[0].click();")   
        time.sleep(5)
    
        #Clic en btn_view_list
        click_element_by_id(driver,wait,By.XPATH, '//*[@id="btn_view_list"]')
        time.sleep(3)
        
        #Clic resetear filtros
        reset = driver.find_element(By.ID, 'btn_reset_filters')
        preloaderEstado = 'block'
        while(preloaderEstado!='none'):
            time.sleep(8)
            preloaderEstado = driver.execute_script("return $('#table_websites_processing').css('display')")
        print(time.strftime("%d/%m/%y - %H:%M:%S") + ' | Escaneando todos los medios de -> ' + tipoMedio)
        dataFinalArr[tipoMedio] =driver.execute_script("""let medios = []; 
                                                        $('#table_websites').DataTable().rows().data().each(function(medio){
                                                            medios.push(medio);
                                                            });
                                                        return medios;""")
    #Transformando los arrays en listas
    dataFinal = []
    for unDataFinal in dataFinalArr:
        dataFinal.extend(dataFinalArr[unDataFinal])

    print(dataFinal)

    for campo_array in ['categorias_agregadas', 'tematicas_no_aceptadas']:
        for idData, data in enumerate(dataFinal):
            if len(data[campo_array]) > 0:
                dataFinal[idData][campo_array + '_arr'] = []
                for categoria in data[campo_array]:
                    dataFinal[idData][campo_array + '_arr'].append(categoria['description'])
            else:
                dataFinal[idData]['categorias_agregadas_arr'] = []
    
    lista = []
    contador = 1
    for medio in dataFinal:
        for dato in ['url_link', 'descripcion', 'idioma', 'idioma_traducido', 'pais_audiencia,da', 'cf', 'dr', 'pa', 'ur', 'tf', 'rd', 'obl', 'precio_post', 'precio_post_cliente', 'max_links_post', 'tipo_sitio', 'tipo_sitio_text', 'crank', 'keywords', 'traffic_organic', 'majestic_links', 'majestic_rd,analytics', 'art_ya_pub', 'aviso_publicidad', 'bl', 'clase_web', 'clase_web_text', 'codigo_analytics', 'codigo_integracion', 'created_at', 'deleted_at', 'discard,favorite', 'fecha_act_ahrefs', 'fecha_act_majestic', 'fecha_act_sistrix,group_check', 'home_appearance', 'image', 'newsletter_difusion', 'ps_rank', 'social_publication', 'tarjetas_rojas', 'texto_conexoo', 'updated_at', 'userId,valoraciones_count', 'visitas_dia']:
            if not dato in medio:
                medio[dato] = None
        for dato in ['categorias_agregadas_arr', 'tematicas_no_aceptadas_arr']:
            if not dato in medio:
                medio[dato] = []

        lista.append(
            (
                medio['id'], 
                medio['url'], 
                medio['url_link'], 
                medio['descripcion'], 
                medio['idioma'], 
                medio['idioma_traducido'], 
                medio['pais_audiencia'], 
                medio['da'], 
                medio['cf'], 
                medio['dr'], 
                medio['pa'], 
                medio['ur'], 
                medio['tf'], 
                medio['rd'], 
                medio['obl'], 
                float(medio['precio_post']), 
                float(medio['precio_post_cliente']), 
                medio['max_links_post'], 
                medio['tipo_sitio'], 
                medio['tipo_sitio_text'], 
                medio['crank'], 
                medio['keywords'], 
                medio['traffic_organic'], 
                medio['majestic_links'], 
                medio['majestic_rd'], 
                medio['art_ya_pub'], 
                medio['aviso_publicidad'], 
                medio['bl'], 
                medio['clase_web'], 
                medio['clase_web_text'], 
                medio['created_at'], 
                medio['discard'], 
                medio['favorite'], 
                medio['group_check'], 
                medio['home_appearance'], 
                medio['image'], 
                medio['newsletter_difusion'],  
                medio['ps_rank'], 
                medio['social_publication'], 
                medio['tarjetas_rojas'], 
                medio['texto_conexoo'], 
                medio['updated_at'], 
                medio['userId'], 
                medio['valoraciones_count'], 
                medio['visitas_dia'], 
                '-|-'.join(medio['categorias_agregadas_arr']), 
                '-|-'.join(medio['tematicas_no_aceptadas_arr'])
            )
        )
        contador += 1
    
    return dataFinal

def guardar_datos(dataFinal):
    for item in dataFinal:
        dato = scraperConexoo(
            id=item['id'],
            url=item['url'],
            url_link=item['url_link'],
            descripcion=item['descripcion'],
            idioma=item['idioma'],
            # idioma_traducido=item['idioma_traducido'],
            pais_audiencia=item['pais_audiencia'],
            da=item['da'],
            # cf=item['cf'],
            # dr=item['dr'],
            # pa=item['pa'],
            # ur=item['ur'],
            # tf=item['tf'],
            # rd=item['rd'],
            # obl=item['obl'],
            precio_post=item['precio_post'],
            precio_post_cliente=item['precio_post_cliente'],
            max_links_post=item['max_links_post'],
            tipo_sitio=item['tipo_sitio'],
            tipo_sitio_text=item['tipo_sitio_text'], 
            # crank=item['crank'],
            # keywords=item['keywords'],
            traffic_organic=item['traffic_organic'],
            # majestic_links=item['majestic_links'],
            # majestic_rd=item['majestic_rd'],
            # art_ya_pub=item['art_ya_pub'],
            # aviso_publicidad=item['aviso_publicidad'],
            # bl=item['bl'],
            # clase_web=item['clase_web'],
            clase_web_text=item['clase_web_text'],
            # created_at=item['created_at'],
            # discard=item['discard'],
            # favorite=item['favorite'],
            # group_check=item['group_check'],
            # home_appearance=item['home_appearance'],
            # image=item['image'],
            # newsletter_difusion=item['newsletter_difusion'],
            # ps_rank=item['ps_rank'],
            # social_publication=item['social_publication'],
            # tarjetas_rojas=item['tarjetas_rojas'],
            # texto_conexoo=item['texto_conexoo'],
            # updated_at=item['updated_at'],
            # userId=['userId'],
            # valoraciones_count=item['valoraciones_count'],
            # visitas_dia=item['visitas_dia'],
            # categorias_agregadas_arr=item['categorias_agregadas_arr'],
            tematicas_no_aceptadas_arr=item['tematicas_no_aceptadas_arr']
        )

        dato.save()
    
if __name__ == '__main__':
    datos = obtener_datos()
    guardar_datos(datos)

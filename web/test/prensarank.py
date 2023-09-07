#%%
import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webjavi.settings.local')
# django.setup()

import time
import json

# from applications.scraperprensarank.models import ScraperPrensarank
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

from scraperlinkbuilding import *

#from applications.scraperprensarank.models import ScraperPrensarank


try:
    # Tomaresmos los datos del json para agilizar los trabajos y tener un lugar donde poder gestionarlo
    print('primer paso')
    def get_config():
        with open('test/config.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
            escanerConfig = dict(data)
    
        return escanerConfig
    
    escanerConfig = get_config()
    driver = crear_driver_chrome(False)
    wait = WebDriverWait(driver, escanerConfig['timeoutSeconds'])

    # Abrir Publisuites
    print('abriendo prensarank')
    driver.get(escanerConfig['prensarankUrl'])
    driver.implicitly_wait(escanerConfig['timeoutSeconds'])
    time.sleep(1)


    # Clic en login de prensarank
    click_element_by_tipo_selector(driver, wait, By.XPATH, '/html/body/div[4]/div[1]/div/nav/div[2]/button[1]')
    time.sleep(1)

    #Accediendo a Prensarank
    escribir_text_en_element_by_tipo_selector(driver,wait,By.NAME,'login_email',escanerConfig['prensarankUser'])
    time.sleep(2)
    escribir_text_en_element_by_tipo_selector(driver,wait,By.NAME, 'login_password',escanerConfig['prensarankPass'])
    time.sleep(2)
    click_element_by_tipo_selector(driver,wait,By.XPATH, '//*[@id="loginForm"]/div[5]/button')
    time.sleep(4)
    click_element_by_tipo_selector(driver,wait,By.XPATH, '//*[@id="main-wrapper"]/div/div/div[3]/div/a[1]')
    time.sleep(1)
    click_element_by_tipo_selector(driver,wait,By.XPATH, '/html/body/div[2]/aside/div/nav/ul/li[2]')
    time.sleep(2)

    # Click en Medios y blogs
    click_element_by_tipo_selector(driver, wait, By.XPATH, '//*[@id="sidebarnav"]/li[2]/a')
    time.sleep(3)
    
except Exception as e:
    print(e)
    print('No se ha podido acceder a Prensarank, el scraper no continua')
    pass


print('segundo paso')

def get_estructura_ths_thead(tr):
    datos = []
    ths = tr.find_elements(By.TAG_NAME, 'th')
    for td in ths:
        datos.append(td.text)

    return datos

def get_estructura_tds_tbody(tr):
    datos = []
    tds = tr.find_elements(By.TAG_NAME, 'td')
    for td in tds:
        datos.append(td.text)

def get_estructura_ths_thead_arr_pos_cabeceras(tr):
    arrPosCabeceras = {}
    contador = 0
    tds = tr.find_elements(By.TAG_NAME, 'th')
    for td in tds:
        arrPosCabeceras[td.text] = contador
        contador += 1

    return arrPosCabeceras

def comprobar_estructora_sin_cambios(estructura):
    estructuraSinCambios = False
    if(estructura == ['NOMBRE', 'PAÍS', 'DR', 'DA', 'CF', 'TF', 'OBL', 'RD', 'TRÁFICO', 'PRECIO', '']):
        estructuraSinCambios = True

    return estructuraSinCambios

def get_list_from_trsBody(trsBody, arrPosCabeceras):
    arrMedios = []
    for tr in trsBody:
        arrMedio = {}
        tds = tr.find_elements_by_tag_name('td')
        arrMedio['NOMBRE'] = tds[arrPosCabeceras['NOMBRE']].text
        arrMedio['PAÍS'] = tds[arrPosCabeceras['PAÍS']].text
        arrMedio['DR'] = tds[arrPosCabeceras['DR']].text
        arrMedio['DA'] = tds[arrPosCabeceras['DA']].text
        arrMedio['CF'] = tds[arrPosCabeceras['CF']].text
        arrMedio['TF'] = tds[arrPosCabeceras['TF']].text
        arrMedio['OBL'] = tds[arrPosCabeceras['OBL']].text
        arrMedio['RD'] = tds[arrPosCabeceras['RD']].text
        arrMedio['TRÁFICO'] = tds[arrPosCabeceras['TRÁFICO']].text
        arrMedio['PRECIO'] = tds[arrPosCabeceras['PRECIO']].text

        buttonInfoWeb = tds[arrPosCabeceras['']].find_element_by_class_name('buttonInfoWeb')

        arrMedio['data-name'] = buttonInfoWeb.get_attribute('data-name')
        arrMedio['data-country'] = buttonInfoWeb.get_attribute('data-country')
        arrMedio['data-country'] = buttonInfoWeb.get_attribute('data-country-name')
        arrMedio['data-url'] = buttonInfoWeb.get_attribute('data-url')
        arrMedio['data-dr'] = buttonInfoWeb.get_attribute('data-dr')
        arrMedio['data-da'] = buttonInfoWeb.get_attribute('data-da')
        arrMedio['data-pa'] = buttonInfoWeb.get_attribute('data-pa')
        arrMedio['data-traffic'] = buttonInfoWeb.get_attribute('data-traffic')
        arrMedio['data-cf'] = buttonInfoWeb.get_attribute('data-cf')
        arrMedio['data-tf'] = buttonInfoWeb.get_attribute('data-tf')
        arrMedio['data-dom'] = buttonInfoWeb.get_attribute('data-dom')
        arrMedio['data-price_user'] = buttonInfoWeb.get_attribute('data-price_user')
        arrMedio['data-ip'] = buttonInfoWeb.get_attribute('data-ip')
        arrMedio['data-in_front_page'] = buttonInfoWeb.get_attribute('data-in_front_page')
        arrMedio['data-promoted'] = buttonInfoWeb.get_attribute('data-promoted')
        arrMedio['data-webid'] = buttonInfoWeb.get_attribute('data-webid')
        arrMedio['data-max_links'] = buttonInfoWeb.get_attribute('data-max_links')
        arrMedios.append(arrMedio)
    
    return arrMedios


def transformar_arr_en_lista_tuplas_prensarank(arr, url_site):
    lista = []

    for medio in arr:
        if not 'lang_filter' in medio:
            medio['lang_filter'] = []
        if not 'category_filter' in medio:
            medio['category_filter'] = []
        
        lista.append(
            (
                medio['id'], 
                medio['name'], 
                medio['url'], 
                url_site, 
                #medio['country']['id'], 
                #medio['country']['iso'], 
                #medio['country']['name'], 
                medio['dr'], 
                medio['da'], 
                medio['cf'], 
                medio['tf'], 
                medio['obl'], 
                medio['dom'], 
                medio['traffic'], 
                medio['price'], 
                medio['pa'], 
                medio['max_links'], 
                medio['max_links_groups'],
                '-|-'.join(medio['lang_filter']),
                '-|-'.join(medio['category_filter']),
                medio['create_groups'], 
                medio['ip'], 
                medio['promoted'], 
                medio['offer'], 
                medio['in_front_page'], 
                medio['is_new'], 
                medio['created_at'], 
                medio['status'], 
                medio['TrType'], 
                medio['type']
            )
        )

    return lista


def js_function_get_medios_prensarank():
    return """
        let medios = []; 
        $('#listTable').DataTable().rows().data().each(function(medio){
            medios.push(medio);
            });
        return medios;
    """

def js_function_get_medios_ids_prensarank():
    return """
        let mediosIds = []; 
        $('#listTable').DataTable().rows().data().each(function(medio){
            mediosIds.push(medio['id']);
            });
        return mediosIds;
    """

def select_change_option(agrupacionSelector, texto, estado):
    return '$(\'select#' + agrupacionSelector + ' option:contains("' + texto + '")\').prop(\'selected\', ' + estado + ').change();'

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


def js_function_get_select_options(selector, valOText):
    js = 'let options = [];'
    js += '$("' + selector + '").each(function(){'
    js += 'options.push($(this).'+ valOText +'().trim());'
    js += '});return options;'

    return js


dataFinal = get_table_data_prensarank(driver, wait=8)

agrupacionesManuales = ['lang_filter', 'category_filter']
agrupacionesDatos = {}
lista_urls = []
for agrupacion in agrupacionesManuales:
    print(f'agrupación--> '+agrupacion)
    # Recoger todos los idiomas/categorias disponibles
    agrupacionesDatos['tipo_' + agrupacion] = driver.execute_script(js_function_get_select_options('#' + agrupacion + ' option', 'text'))
    print('haciendo el for de agrupoaciones manuales')
    if agrupacion == 'lang_filter':
        for elem in escanerConfig['prensarankLangFilterExcluir']:
            if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)
            print('haciendo el if de agrupación y sus variantes')
    elif agrupacion == 'category_filter':
        for elem in escanerConfig['prensarankCategoryFilterExcluir']:
            if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)
            print('haciendo el if de category')
    # Cargar cada idioma/categoria y recoger las ids de los medios que aparecen en la tabla por cada filtro de cada idioma
    agrupacionesDatos['tipo_ids_' + agrupacion] = {}
    for agrupacionTipo in agrupacionesDatos['tipo_' + agrupacion]:
        driver.execute_script(select_change_option(agrupacion, agrupacionTipo, 'true'))
        time.sleep(2)
        print(time.strftime("%d/%m/%y - %H:%M:%S") + ' | Escaneando ' + agrupacion + ' -> ' + agrupacionTipo)
        agrupacionesDatos['tipo_ids_' + agrupacion][agrupacionTipo] = get_table_data_ids_prensarank(driver, wait=10)
        time.sleep(2)
        driver.execute_script(select_change_option(agrupacion, agrupacionTipo, 'false'))
        time.sleep(2)
  
            # Recorrer cada agrupación una vez y crear una lista auxiliar con los ids de cada medio con el grupo/grupos al que pertenece (opción más eficiente)
            # Que luego por cada id recorrer cada agrupación (Idioma/Categoría) para ver si está dentro

    print('vamos a por las agrupaciones')
    agrupacionesDatos['tipo_ids_' + agrupacion] = {}
    for datoAgrupacion in agrupacionesDatos['tipo_ids_' + agrupacion]:
        for idMedio in agrupacionesDatos['tipo_ids_' + agrupacion][datoAgrupacion]:
            if not idMedio in agrupacionesDatos['tipo_ids_' + agrupacion]:
                agrupacionesDatos['tipo_ids_' + agrupacion][idMedio] = []
            agrupacionesDatos['tipo_ids_' + agrupacion][idMedio].append(datoAgrupacion)
            print('último for acabado')



for idData, data in enumerate(dataFinal):
    for agrupacion in agrupacionesManuales:
        if dataFinal[idData]['id'] in agrupacionesDatos['tipo_ids_' + agrupacion]:
            if not agrupacion in dataFinal[idData]:
                dataFinal[idData][agrupacion] = []
            dataFinal[idData][agrupacion].extend(agrupacionesDatos['tipo_ids' + agrupacion][dataFinal[idData]['id']])       
    


try:
    dataFinalTuplas = transformar_arr_en_lista_tuplas_prensarank(dataFinal, "https://prensarank.com/")
    df = pd.DataFrame(dataFinalTuplas, columns=['id',
                                                'name',
                                                'url',
                                                'urls_site',
                                                'dr', 
                                                'da', 
                                                'cf', 
                                                'tf', 
                                                'obl', 
                                                'dom', 
                                                'traffic', 
                                                'price', 
                                                'pa', 
                                                'max_links', 
                                                'max_links_groups',
                                                'lang_filter',
                                                'category_filter',
                                                'create_groups', 
                                                'ip', 
                                                'promoted', 
                                                'offer', 
                                                'in_front_page', 
                                                'is_new', 
                                                'created_at', 
                                                'status', 
                                                'TrType', 
                                                'type'
                                            ])
    # for item in dataFinalTuplas:
    #     dato = ScraperPrensarank(
    #                     name=item['name'],
    #                     url=item['url'],
    #                     urls_site=item['urls_site'],
    #                     dr=item['dr'],
    #                     da=item['da'],
    #                     cf=item['cf'],
    #                     tf=item['tf'],
    #                     traffic=item['traffic'],
    #                     price=item['price'],
    #                     max_links=item['max_links'],
    #                     max_links_groups=item['max_links_groups'],
    #                     )
    #     print(dato)
    #     dato.save()
except Exception as e:
    print(e)
print(df)
#%%



    #%%
    # agrupacionesManuales = ['lang_filter', 'category_filter']
    # agrupacionesDatos = {}
    # lista_urls = []
    # for agrupacion in agrupacionesManuales:
    #     # Recoger todos los idiomas/categorias disponibles
    #     agrupacionesDatos['tipo_' + agrupacion] = driver.execute_script(js_function_get_select_options('#' + agrupacion + ' option', 'text'))

    #     if agrupacion == 'lang_filter':
    #         for elem in escanerConfig['prensarankLangFilterExcluir']:
    #             if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)
    #     elif agrupacion == 'category_filter':
    #         for elem in escanerConfig['prensarankCategoryFilterExcluir']:
    #             if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)

    #     # Cargar cada idioma/categoria y recoger las ids de los medios que aparecen en la tabla por cada filtro de cada idioma
    #     agrupacionesDatos['tipo_ids_' + agrupacion] = {}
    #     for agrupacionTipo in agrupacionesDatos['tipo_' + agrupacion]:
    #         driver.execute_script(select_change_option(agrupacion, agrupacionTipo, 'true'))
    #         time.sleep(2)
    #         print(time.strftime("%d/%m/%y - %H:%M:%S") + ' | Escaneando ' + agrupacion + ' -> ' + agrupacionTipo)
    #         agrupacionesDatos['tipo_ids_' + agrupacion][agrupacionTipo] = get_table_data_ids_prensarank(driver, wait=10)
    #         time.sleep(2)
    #         driver.execute_script(select_change_option(agrupacion, agrupacionTipo, 'false'))
    #         time.sleep(2)

    #     # Recorrer cada agrupación una vez y crear una lista auxiliar con los ids de cada medio con el grupo/grupos al que pertenece (opción más eficiente)
    #     # Que luego por cada id recorrer cada agrupación (Idioma/Categoría) para ver si está dentro
    #     agrupacionesDatos['tipo_ids_' + agrupacion] = {}
    #     for datoAgrupacion in agrupacionesDatos['tipo_ids_' + agrupacion]:
    #         for idMedio in agrupacionesDatos['tipo_ids_' + agrupacion][datoAgrupacion]:
    #             if not idMedio in agrupacionesDatos['tipo_ids_' + agrupacion]:
    #                 agrupacionesDatos['tipo_ids_' + agrupacion][idMedio] = []
    #             agrupacionesDatos['tipo_ids_' + agrupacion][idMedio].append(datoAgrupacion)
    #         print(datoAgrupacion)
    # # %%
    # for idData, data in enumerate(dataFinal):
    #     for agrupacion in agrupacionesManuales:
    #         if dataFinal[idData]['id'] in agrupacionesDatos['tipo_ids_' + agrupacion]:
    #             if not agrupacion in dataFinal[idData]:
    #                 dataFinal[idData][agrupacion] = []
    #             dataFinal[idData][agrupacion].extend(agrupacionesDatos['tipo_ids' + agrupacion][dataFinal[idData]['id']])
    #%%
   
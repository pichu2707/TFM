import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webjavi.settings.local')

django.setup()

import time
import json
import time
from os import name
import json

from applications.scraperteblogueo.models import ScraperTeblogueo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


import pandas as pd
from scraperlinkbuilding import *

# Tomaresmos los datos del json para agilizar los trabajos y tener un lugar donde poder gestionarlo

def obtener_datos():
    escanerConfig = get_config()
    driver = crear_driver_chrome(True)
    wait = WebDriverWait(driver, escanerConfig['timeoutSeconds'])

    # Abrir Teblogueo
    print('abriendo tebloguo')
    driver.get(escanerConfig['teblogueoUrl'])
    driver.implicitly_wait(escanerConfig['timeoutSeconds'])
    time.sleep(1)

    #Accediendo a Conexoo
    escribir_text_en_element_by_tipo_selector(driver, wait, By.XPATH,"//input[@name='username']", escanerConfig['teblogueoUser'])
    time.sleep(1)
    escribir_text_en_element_by_tipo_selector(driver, wait,By.XPATH,"//input[@name='password']", escanerConfig['teblogueoPass'])
    time.sleep(1)
    click_element_by_tipo_selector(driver,wait,By.XPATH,"//button[normalize-space()='ENTRAR']")

    def js_function_aceptar_aviso_sin_saldo_teblogueo():
        return """if($('span:contains("Parece que no tienes saldo, para poder operar en la plataforma como Agencia es necesario disponer de")').length > 0){
            $('span:contains("Parece que no tienes saldo, para poder operar en la plataforma como Agencia es necesario disponer de")').parent().parent().find('button:contains("Aceptar")').click();
        }
        """
    driver.execute_script(js_function_aceptar_aviso_sin_saldo_teblogueo())

    click_element_by_tipo_selector(driver, wait, By.XPATH, '/html/body/div[1]/section/div[2]/div[2]/div[1]/div/div[2]/div/form/div/div[15]/div[2]/button')

    def js_function_get_medios_teblogueo():
        return """
            let medios = []; 
            $('#tabla_medios_general').DataTable().rows().data().each(function(medio){
                medios.push(medio);
                });
            return medios;
        """

    def select_change_option_attr_nice_select(agrupacionSelector, texto, estado):
        return '$(\'#' + agrupacionSelector + ' option:contains("' + texto + '")\').attr(\'selected\', \'' + estado + '\');$(\'#' + agrupacionSelector + '\').niceSelect(\'update\');'
    
    def js_function_desactivar_check_teblogeo(selector):
        return "if($('" + selector + "').hasClass('active')){$('" + selector + "').click();}"
    
    def select_change_option_attr_nice_select(agrupacionSelector, texto, estado):
        return '$(\'#' + agrupacionSelector + ' option:contains("' + texto + '")\').attr(\'selected\', \'' + estado + '\');$(\'#' + agrupacionSelector + '\').niceSelect(\'update\');'
    
    def js_function_activar_check_teblogeo(selector):
        return "if(!$('" + selector + "').hasClass('active')){$('" + selector + "').click();}"
    
    def js_function_get_select_options(selector, valOText):
        js = 'let options = [];'
        js += '$("' + selector + '").each(function(){'
        js += 'options.push($(this).'+ valOText +'().trim());'
        js += '});return options;'

        return js
    
    def js_function_get_medios_ids_teblogueo():
        return """
            let mediosIds = []; 
            $('#tabla_medios_general').DataTable().rows().data().each(function(medio){
                mediosIds.push(medio['pk']);
                });
            return mediosIds;
        """

    print(time.strftime("%d/%m/%y - %H:%M:%S") + ' | Escaneando todos los medios')
    dataFinal = driver.execute_script(js_function_get_medios_teblogueo())

    agrupacionesManualesSelects = ['language', 'blog_topics', 'country', 'link_type']
    agrupacionesDatos = {}

    for agrupacion in agrupacionesManualesSelects:

        # Restablecer el filtro
        driver.execute_script(select_change_option_attr_nice_select('language', 'Todos los idiomas', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('blog_topics', 'Todas las temáticas', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('country', 'Todos los países', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('sponsored_mark', 'Indiferente', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('link_type', 'Indiferente', 'selected'))

        for check in ['#check_0', '#check_1', '#check_2', '#check_3']:
            driver.execute_script(js_function_desactivar_check_teblogeo(check))

        # Recoger todos los idiomas/categorias disponibles
        agrupacionesDatos['tipo_' + agrupacion] = driver.execute_script(js_function_get_select_options('#' + agrupacion + ' option', 'text'))

        if agrupacion == 'language':
            for elem in escanerConfig['teBlogueoLanguageExcluir']:
                if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)
        elif agrupacion == 'blog_topics':
            for elem in escanerConfig['teBlogueoBlogTopicsExcluir']:
                if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)
        elif agrupacion == 'country':
            auxList = []
            for elem in agrupacionesDatos['tipo_' + agrupacion]:
                if elem in escanerConfig['teBlogueoCountryIncluir']: auxList.append(elem)
            agrupacionesDatos['tipo_' + agrupacion] = auxList.copy()
        elif agrupacion == 'link_type':
            for elem in escanerConfig['teBlogueoLinkTypeExcluir']:
                if elem in agrupacionesDatos['tipo_' + agrupacion]: agrupacionesDatos['tipo_' + agrupacion].remove(elem)

        # Cargar cada idioma/categoria y recoger las ids de los medios que aparecen en la tabla por cada filtro de cada idioma
        agrupacionesDatos['ids_tipo_' + agrupacion] = {}
        for agrupacionTipo in agrupacionesDatos['tipo_' + agrupacion]:
            # Elegir idioma o categoría

            driver.execute_script(select_change_option_attr_nice_select(agrupacion, agrupacionTipo, 'selected'))
            time.sleep(1)
            # Click en Aplicar Filtro
            filtro1 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div[2]/div[2]/div[1]/div/div[2]/div/form/div/div[15]/div[2]/button')
            filtro1.click()
            time.sleep(5)

            print(time.strftime("%d/%m/%y - %H:%M:%S") + ' | Escaneando ' + agrupacion + ' -> ' + agrupacionTipo)
            agrupacionesDatos['ids_tipo_' + agrupacion][agrupacionTipo] = driver.execute_script(js_function_get_medios_ids_teblogueo())
            time.sleep(2)


        # Recorrer cada agrupación una vez y crear una lista auxiliar con los ids de cada medio con el grupo/grupos al que pertenece (opción más eficiente)
        # Que luego por cada id recorrer cada agrupación (Idioma/Categoría) para ver si está dentro
        agrupacionesDatos['ids_tipo_' + agrupacion] = {}
        for datoAgrupacion in agrupacionesDatos['ids_tipo_' + agrupacion]:
            for idMedio in agrupacionesDatos['ids_tipo_' + agrupacion][datoAgrupacion]:
                if not idMedio in agrupacionesDatos['ids_tipo_' + agrupacion]:
                    agrupacionesDatos['ids_tipo_' + agrupacion][idMedio] = []
                agrupacionesDatos['ids_tipo_' + agrupacion][idMedio].append(datoAgrupacion)

    
    agrupacionesManualesChecks = ['medioTematico', 'medioTipo']

    for agrupacion in agrupacionesManualesChecks:

        # Restablecer el filtro
        driver.execute_script(select_change_option_attr_nice_select('language', 'Todos los idiomas', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('blog_topics', 'Todas las temáticas', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('country', 'Todos los países', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('sponsored_mark', 'Indiferente', 'selected'))
        driver.execute_script(select_change_option_attr_nice_select('link_type', 'Indiferente', 'selected'))

        for check in ['#check_0', '#check_1', '#check_2', '#check_3']:
            driver.execute_script(js_function_desactivar_check_teblogeo(check))

        # Set tipo checks
        if agrupacion == 'medioTematico':
            agrupacionesDatos['tipo_' + agrupacion] = ['check_0', 'check_1']
        elif agrupacion == 'medioTipo':
            agrupacionesDatos['tipo_' + agrupacion] = ['check_2', 'check_3']

        # Cargar cada idioma/categoria y recoger las ids de los medios que aparecen en la tabla por cada filtro de cada idioma
        agrupacionesDatos['ids_tipo_' + agrupacion] = {}
        for agrupacionTipoTemp in agrupacionesDatos['tipo_' + agrupacion]:

            if agrupacionTipoTemp == 'check_0':
                agrupacionTipo = 'General'
            elif agrupacionTipoTemp == 'check_1':
                agrupacionTipo = 'Temático'
            elif agrupacionTipoTemp == 'check_2':
                agrupacionTipo = 'Blog'
            elif agrupacionTipoTemp == 'check_3':
                agrupacionTipo = 'Periódico'

            # Click en check
            driver.execute_script(js_function_activar_check_teblogeo('#' + agrupacionTipoTemp))
            time.sleep(1)

            # Aplicar filtro
            filtro1 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div[2]/div[2]/div[1]/div/div[2]/div/form/div/div[15]/div[2]/button')
            filtro1.click()
            time.sleep(5)


            print(time.strftime("%d/%m/%y - %H:%M:%S") + ' | Escaneando ' + agrupacion + ' -> ' + agrupacionTipo)
            agrupacionesDatos['ids_tipo_' + agrupacion][agrupacionTipo] = driver.execute_script(js_function_get_medios_ids_teblogueo())
            time.sleep(2)


        # Recorrer cada agrupación una vez y crear una lista auxiliar con los ids de cada medio con el grupo/grupos al que pertenece (opción más eficiente)
        # Que luego por cada id recorrer cada agrupación (medioTematico/medioTipo) para ver si está dentro
        agrupacionesDatos['ids_tipo_' + agrupacion] = {}
        for datoAgrupacion in agrupacionesDatos['ids_tipo_' + agrupacion]:
            for idMedio in agrupacionesDatos['ids_tipo_' + agrupacion][datoAgrupacion]:
                if not idMedio in agrupacionesDatos['ids_tipo_' + agrupacion]:
                    agrupacionesDatos['ids_tipo_' + agrupacion][idMedio] = []
                agrupacionesDatos['ids_tipo_' + agrupacion][idMedio].append(datoAgrupacion)


    agrupacionesManuales = []
    agrupacionesManuales.extend(agrupacionesManualesSelects)
    agrupacionesManuales.extend(agrupacionesManualesChecks)

    for idData, data in enumerate(dataFinal):
        for agrupacion in agrupacionesManuales:
            if dataFinal[idData]['pk'] in agrupacionesDatos['ids_tipo_' + agrupacion]:
                if not agrupacion in dataFinal[idData]['fields']:
                    dataFinal[idData]['fields'][agrupacion] = []
                dataFinal[idData]['fields'][agrupacion].extend(agrupacionesDatos['ids_tipo_' + agrupacion][dataFinal[idData]['pk']])
    
    def transformar_arr_en_lista_tuplas_teblogeo(arr, url_site):
        lista = []

        for medio in arr:
            if not 'language' in medio['fields']:
                medio['fields']['language'] = []
            if not 'blog_topics' in medio['fields']:
                medio['fields']['blog_topics'] = []
            if not 'country' in medio['fields']:
                medio['fields']['country'] = []
            if not 'link_type' in medio['fields']:
                medio['fields']['link_type'] = []
            if not 'medioTematico' in medio['fields']:
                medio['fields']['medioTematico'] = []
            if not 'medioTipo' in medio['fields']:
                medio['fields']['medioTipo'] = []
            if not 'DR' in medio['fields']:
                medio['fields']['DR'] = None
            if not 'UR' in medio['fields']:
                medio['fields']['UR'] = None
            
            lista.append(
                (
                    medio['pk'], 
                    medio['fields']['name'],
                    medio['fields']['url'], 
                    url_site, 
                    medio['fields']['DA'], 
                    medio['fields']['DF'], 
                    medio['fields']['DR'], 
                    medio['fields']['PA'], 
                    medio['fields']['UR'], 
                    medio['fields']['trust_flow'], 
                    medio['fields']['is_mine'], 
                    medio['fields']['is_offer'], 
                    medio['fields']['max_links'], 
                    medio['fields']['poffer_pvp'], 
                    medio['fields']['ppvp'], 
                    medio['fields']['visits_month'], 
                    medio['fields']['sponsored_mark'], 
                    medio['fields']['link_type'],
                    '-|-'.join(medio['fields']['language']), 
                    '-|-'.join(medio['fields']['blog_topics']), 
                    '-|-'.join(medio['fields']['country']), 
                    '-|-'.join(medio['fields']['link_type']), 
                    '-|-'.join(medio['fields']['medioTematico']), 
                    '-|-'.join(medio['fields']['medioTipo']), 
                    medio['model']
                )
            )
        print(f' esto es la lista --> {lista}')
        


        dataFinalTuplas = transformar_arr_en_lista_tuplas_teblogeo(dataFinal, escanerConfig['teblogueoUrl'])
        columns_name = ['id','nombre','url_link','url_site', 'DA', 'DF','DR', #0-6
        'PA','UR','trust_flow','is_mine','is_offer','max_links','peffer_pvp','ppvp','visits_month','sponsored_mark', 'link_type',#7-17
        'language','blog_topics','country','link_type', #18-21
        'medioTematico','medioTipo','model'] #22-24

        df = pd.DataFrame(dataFinalTuplas, columns=columns_name)
        print(df)
        return lista
    print(f' el print de dataFinal --> {dataFinal}')
    return dataFinal

def guardar_datos(dataFinal):
    datos_temporales = []
    for item in dataFinal:
        dato = ScraperTeblogueo(
                        name=item['fields']['name'],
                        url=item['fields']['url'],
                        trust_flow = item['fields']['trust_flow'],
                        visits_month = item['fields']['visits_month'],
                        peffer_pvp = item['fields']['poffer_pvp'],
                        ppvp=item['fields']['ppvp'],
                        max_links=item['fields']['max_links'],
                        sponsored_mark = item['fields']['sponsored_mark'],
                        model = item['model'],
                        
                        # name = item[1],  
                        # url = item[2],
                        # trust_flow = item[9],
                        # visits_month = item[15],
                        # peffer_pvp = item[13],
                        # ppvp = item[14],
                        # max_links = item[12],
                        # sponsored_mark = item[16],
                        # model = item[24],
                    )   
                  # Añadir el nuevo registro a la lista temporal
        datos_temporales.append(dato)    
    # Una vez que todos los datos se han añadido a la lista temporal,
    # borrar los registros antiguos.
    ScraperTeblogueo.objects.all().delete()
    for dato in datos_temporales:
        dato.save()
        
if __name__== '__main__':
    datos = obtener_datos()
    guardar_datos(datos)
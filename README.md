# Webjavi: scraping de marketplaces de link building con Django

Aplicación web en Django y scrapers en Selenium que extraen los catálogos de plataformas de compraventa de enlaces SEO (Prensarank, Teblogueo y Conexoo) para mostrarlos y compararlos en un único lugar.

> Trabajo Fin de Máster (EIP, Escuela Internacional de Posgrados), 2023. Memoria completa en [`docs/`](docs/TFM_FranciscoJavierLazaro.docx.pdf).

**Nota:** es un prototipo (MVP) académico. Incluye una sección de retrospectiva técnica sobre sus errores de diseño: [ir a la retrospectiva](#retrospectiva-errores-de-estructura-y-qué-haría-hoy).

## Contexto

**Link building.** Una parte del posicionamiento SEO consiste en conseguir enlaces desde otras webs. Existen marketplaces donde se compran artículos patrocinados en medios y blogs. Cada plataforma publica su propio catálogo con métricas de autoridad (DA, DR, CF, TF), tráfico y precio, y un mismo medio puede aparecer en varias con precios distintos.

**Problema.** Comparar a mano esos catálogos es lento y poco reproducible. La memoria lo plantea como un proyecto sin cierre: las plataformas cambian su código con el tiempo y aparecen otras nuevas, por lo que el valor está en automatizar la captura y poder construir filtros y, a futuro, un histórico de precios.

**Contexto académico.** Trabajo Fin de Máster de 2023. El autor lo eligió en lugar de una de las propuestas estándar por dos motivos que cita la memoria: cubría casi todos los bloques del máster y servía de base para su web personal (blog y portfolio) con herramientas propias de SEO.

**Objetivos declarados en la memoria**

- Construir una aplicación web en Django con un blog (SEO, CRO, Python) y una sección de herramientas.
- Extraer datos de varias plataformas de venta de enlaces, empezando en notebooks y migrando el código a Django.
- Mostrar los datos al usuario registrado, con filtros por rango de tráfico y por DR, y permitirle guardar favoritos.
- Dejarlo preparado para escalar a más plataformas y comparar precios cuando haya enlaces comunes.

## Qué hace el proyecto

### Parte de investigación (notebooks)

Los notebooks de [`notebooks/`](notebooks/) prototiparon cada scraper con Selenium (login, paginación, extracción) antes de pasarlos a scripts. Los datos capturados están en `notebooks/data/` (CSV de Prensarank, Teblogueo, Conexoo y Publisuites, del orden de miles de filas cada uno; la memoria habla de "varios miles de filas").

`Comparativa.ipynb` hace un cruce (`merge` externo por URL) de los CSV de Conexoo, Publisuites y Prensarank para ver el mismo medio en varias plataformas y resaltar el precio más bajo. Es un análisis exploratorio, no un estudio cerrado.

> La memoria no contiene un análisis comparativo con cifras ni conclusiones numéricas sobre qué plataforma es mejor. Sus conclusiones son de proceso: Django exige trabajar bien el modelo de datos y sus relaciones, y el proyecto seguirá creciendo como herramienta personal. No se atribuyen aquí resultados que el documento no recoge.

### Aplicación web (Django)

Estado real del código:

| Área | Estado |
|------|--------|
| Prensarank | Modelo, scraper y listado paginado (`/prensarank/`) conectados de extremo a extremo |
| Teblogueo | Modelo y scraper. La vista es un esqueleto y no está incluida en `webjavi/urls.py` |
| Conexoo | Modelo y scraper. Vista sin terminar y sin `urls.py` |
| Blog | Apps `entrada` y `home`, edición con CKEditor, sitemap |
| Usuarios | Modelo de usuario propio (`applications/users`) |
| Favoritos | App `favoritos` para guardar medios |
| Publisuites, SEOlyze | Solo en notebooks, sin scraper en `scrapers/` |

## Arquitectura

```text
 Plataformas (Prensarank, Teblogueo, Conexoo)
        │  Selenium (login + paginación)
        ▼
  scrapers/*.py ── django.setup() ──► ORM ──► PostgreSQL
                                                  │
                                       applications/scraper*/views.py
                                                  ▼
                                         templates/ (listados)

 notebooks/*.ipynb ──► notebooks/data/*.csv ──► Comparativa.ipynb
```

1. Cada script de `scrapers/` abre Chrome con Selenium, inicia sesión con las credenciales de `config.json` y recorre el catálogo.
2. Los helpers comunes (driver, clics, escritura, lectura de config) están en `scrapers/scraperlinkbuilding.py`.
3. El script inicializa Django (`django.setup()`) y guarda los registros con el ORM en el modelo de su plataforma.
4. Las vistas de Django (`ListView`) leen esos modelos. Los notebooks trabajan en paralelo sobre CSV.

La configuración se divide en `webjavi/settings/{base,local,prod}.py` y las apps viven bajo `applications/`.

## Stack

| Área | Tecnología |
|------|------------|
| Backend | Django 4.2, django-ckeditor, django-environ, django-model-utils, Pillow |
| Base de datos | PostgreSQL (psycopg2) |
| Scraping | Selenium 4, webdriver-manager |
| Análisis | pandas, numpy, Jupyter |

## Estructura del repositorio

```text
.
├── manage.py
├── applications/            # Apps de Django
│   ├── home/                #   portada, contacto, sitemap
│   ├── users/               #   usuario personalizado
│   ├── entrada/             #   blog
│   ├── favoritos/           #   medios favoritos
│   ├── scraperprensarank/   #   modelo + listado (completo)
│   ├── scraperteblogueo/    #   solo modelo
│   └── scraperconexoo/      #   solo modelo
├── scrapers/                # Scripts Selenium (guardan vía ORM)
│   └── scraperlinkbuilding.py  # helpers compartidos
├── webjavi/                 # Proyecto Django (urls, wsgi, settings/)
├── templates/  static/  media/
├── notebooks/               # Prototipos y comparativa
│   └── data/                #   CSV capturados
├── docs/                    # Memoria del TFM (PDF)
├── config.example.json      # Credenciales y filtros de los scrapers
├── requirements.txt
└── requirements-notebooks.txt
```

## Puesta en marcha

Requiere Python 3.9 (las versiones fijadas de pandas y numpy no instalan en 3.10 o superior), PostgreSQL y Chrome (para los scrapers).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Variables de entorno en `.env` (en la raíz). El archivo `.env.example` contiene:

```dotenv
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=webjavi
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```

```bash
cp .env.example .env                  # editar SECRET_KEY y datos de BD
cp config.example.json config.json    # solo para los scrapers

createdb webjavi                      # o el nombre indicado en DB_NAME
python manage.py migrate
python manage.py runserver
```

Se necesita PostgreSQL: varios modelos declaran `CharField` sin `max_length`, algo que SQLite no admite al migrar.

Para ejecutar un scraper, desde la raíz y con `config.json` completo:

```bash
python -m scrapers.prensarank
python -m scrapers.teblogueo
python -m scrapers.conexoo
```

Notebooks:

```bash
pip install -r requirements-notebooks.txt
jupyter notebook notebooks/
```

**Conflicto de dependencias resuelto.** El proyecto original fijaba `requests==2.23.0` junto a `selenium==4.10.0`, que declaran requisitos incompatibles sobre `urllib3`. `requirements.txt` usa ahora `requests==2.31.0`, que instala en Python 3.9; se discute en la retrospectiva.

Las credenciales que aparecían en los notebooks originales se sustituyeron por `***REDACTED***`.

## Retrospectiva: errores de estructura y qué haría hoy

Mirando el proyecto con la experiencia de hoy, estos son los problemas de diseño que identifico. Los verifiqué contra el código actual; cada fila indica dónde se ve.

### Diseño y arquitectura

| Problema (dónde) | Por qué es un problema | Qué haría hoy |
|---|---|---|
| Una app y un modelo Django por plataforma: `applications/scraperprensarank`, `scraperteblogueo`, `scraperconexoo` | El objetivo era comparar plataformas y cada una tiene su esquema (`name`/`nombre`, `price`/`precio_post`, `ppvp`...). Hay modelos, vistas y plantillas duplicados y no se puede consultar "este medio en todas las plataformas" con una sola query | Un modelo normalizado `Medio` y otro `Oferta` con campo `platform`, precio y métricas tipadas. Las diferencias de cada plataforma se resuelven en el adaptador, no en la base de datos |
| Scrapers acoplados a Django y a un script por plataforma: `scrapers/*.py` hacen `django.setup()` y guardan con el ORM; `obtener_datos()` es una función de 150 a 325 líneas con funciones anidadas | Mezcla navegación, parseo y persistencia. No se puede probar el parseo sin navegador y base de datos, y cada plataforma repite la estructura | Separación hexagonal: dominio (`Medio`, `Oferta`), puerto `MarketplaceScraper` y un adaptador Selenium por plataforma. Ejecución mediante un `management command` y, si hace falta periodicidad (la memoria menciona cada 15 días), una cola de tareas como Celery |
| Duplicación entre los tres scrapers: `time.sleep` encadenados (9 a 14 por script), mismo flujo de login y paginación copiado | Cualquier cambio en el flujo se toca tres veces; los sleeps fijos hacen los scrapers lentos y frágiles | Una clase base o *strategy* con login, paginación y espera explícita (`WebDriverWait`) compartidos. Los helpers actuales de `scraperlinkbuilding.py` son un buen punto de partida, pero quedaron a medias |
| Métricas numéricas guardadas como texto: `ScraperPrensarank.dr/da/traffic/price` son `CharField(max_length=3..9)` | No se puede filtrar por rango de tráfico ni por DR, que era un objetivo de la memoria. `url` con `max_length=50` rompe con URLs largas | `PositiveIntegerField`/`DecimalField` para métricas y precio, y `URLField` con longitud adecuada |
| `CharField` sin `max_length`: `scraperteblogueo/models.py`, `scraperconexoo/models.py` | Solo PostgreSQL lo admite; ata el proyecto a un motor sin haberlo decidido | Usar `TextField` o fijar `max_length` y validarlo. Elegir el motor de forma consciente |
| Sin `unique` real en los modelos de Teblogueo y Conexoo (la constraint de Conexoo está comentada) | Cada ejecución del scraper puede duplicar filas, y no existe histórico de precios (que la memoria menciona como objetivo) | Clave natural (`platform` + URL) con *upsert*, y una tabla de precios con fecha para el histórico |

### Código y calidad

| Problema (dónde) | Por qué es un problema | Qué haría hoy |
|---|---|---|
| Copy-paste sin revisar: `applications/scraperconexoo/views.py` define `class Prensarank`; `scraperteblogueo/views.py` tiene `MODEL_NAMEListView` y su `urls.py` apunta a `views.ListTeblogueo`, que no existe; `scraperconexoo` no tiene `urls.py` | Código muerto o roto que da una falsa idea de funcionalidad completa | Vertical slices pequeños: no crear la app hasta tener vista, URL y plantilla funcionando |
| Selectores XPath absolutos y sin reintentos: 25 usos de XPath en `scrapers/` (por ejemplo `/html/body/div[4]/div[1]/div/nav/div[2]/button[1]` en `prensarank.py`) | Cualquier cambio de maquetación rompe el scraper; no hay *retry* ni límite de ritmo | Selectores por atributo o `data-*`, reintentos con *backoff*, límite de peticiones y detección explícita de cambios de estructura |
| API de Selenium obsoleta: `scrapers/prensarank.py` líneas 91 y 103 usan `find_elements_by_tag_name` y `find_element_by_class_name`, eliminadas en Selenium 4.3, mientras `requirements.txt` fija 4.10 | Esa ruta fallaría al ejecutarse con la versión fijada | Usar `find_element(By..., ...)` y cubrir el parseo con pruebas sobre HTML guardado |
| Sin tests: los `tests.py` de las apps son los generados por Django, sin casos | No hay red de seguridad para refactorizar ni para detectar que una plataforma cambió | Pruebas unitarias del parseo con HTML de ejemplo, de los modelos y de las vistas; CI desde el primer día |
| Notebook comparativo frágil: `notebooks/Comparativa.ipynb` lee los CSV con rutas relativas (`conexoo.csv`) que no coinciden con `notebooks/data/`, y resalta el mínimo por fila sobre todas las columnas, no solo las de precio | La comparación central del proyecto no es reproducible ni correcta | Normalizar primero un esquema común (`platform`, `url`, `price`), cargar desde `data/` y comparar solo precios |

### Dependencias, seguridad y organización

| Problema (dónde) | Por qué es un problema | Qué haría hoy |
|---|---|---|
| Dependencias antiguas y en conflicto: `requests==2.23.0` frente a `selenium==4.10.0` (corregido después a `requests==2.31.0`); pandas 1.2.3 obliga a Python 3.9; `beautifulsoup4` sin versión en `requirements-notebooks.txt` | Entorno difícil de reproducir, con riesgo de seguridad por versiones antiguas | `pip-tools` o `uv` con *lock file*, versiones compatibles y Jupyter separado del runtime (ya separado en un segundo archivo, pero tarde) |
| Credenciales y entorno dentro del repositorio al inicio. Hoy el historial está limpio, pero la limpieza fue posterior: `.gitignore` se añadió en 2026 (`39ab4ce`) y los notebooks conservan marcas `***REDACTED***` (`be64b2d`) | Un secreto subido sigue comprometido aunque se reescriba el historial; hay que rotarlo | `.gitignore` y variables de entorno desde el primer commit; `.env.example` versionado; un escáner de secretos como pre-commit |
| Credenciales de prueba del panel de administración en el anexo de la propia memoria (`docs/TFM_FranciscoJavierLazaro.docx.pdf`, p. 15) | Mismo problema: un dato sensible en un documento público | Entregar credenciales por un canal aparte o usar datos de demo que no existan en ningún entorno real |
| Estructura de carpetas improvisada: historial con "resubiendo el proyecto por problemas de carpetas mal colocadas" (`1f8a79f`) y reorganización posterior para llevar el proyecto Django a la raíz (`591af8a`); el proyecto original estaba anidado | Fricción para clonar, ejecutar y revisar | Plantilla de proyecto clara desde el inicio: `manage.py` en la raíz, `src` o `applications`, `docs`, `notebooks` |
| Scraping sin análisis legal: se automatiza el login en servicios de terceros y se esquiva el captcha (la memoria lo llama "su lado hacking") | Los términos de uso de esas plataformas pueden prohibirlo; los datos son de acceso privado tras el login | Revisar los ToS antes de empezar, preferir APIs o acuerdos, y respetar límites de ritmo |
| Datos y *logs* sin tratamiento: CSV capturados versionados en el repositorio | Pesan, caducan y pueden contener datos de acceso restringido | Mantener los datos fuera de git (almacenamiento externo o DVC) y publicar solo muestras |

### Lo que sí funcionó

- Prototipar en notebooks y pasar a scripts: permitió validar cada scraper por partes.
- Separar `settings` en `base`, `local` y `prod`, y agrupar las apps bajo `applications/`.
- Un helper común de driver y configuración (`scraperlinkbuilding.py`) y logs de ejecución.
- Elegir un problema real, con datos reales de varios miles de filas por plataforma, en lugar de un ejemplo de manual.

## Estado del proyecto

Proyecto académico de 2023, publicado como muestra de trabajo y no mantenido. Las plataformas rastreadas pueden haber cambiado su interfaz, por lo que los selectores de los scrapers probablemente ya no funcionen. Si lo retomara, empezaría por el modelo normalizado y los tests descritos arriba.

## Documentación

Memoria del trabajo: [`docs/TFM_FranciscoJavierLazaro.docx.pdf`](docs/TFM_FranciscoJavierLazaro.docx.pdf).

## Autor

Francisco Javier Lázaro. GitHub: [@pichu2707](https://github.com/pichu2707)

# Webjavi: scraping de marketplaces de link building con Django

Aplicación web en Django y scrapers en Selenium que extraen los catálogos de plataformas de compraventa de enlaces SEO (Prensarank, Teblogueo y Conexoo) para mostrarlos y compararlos en un único lugar.

> Trabajo Fin de Máster (EIP, Escuela Internacional de Posgrados), 2023. Memoria completa en [`docs/`](docs/TFM_FranciscoJavierLazaro.docx.pdf).

## Contexto

**Link building.** Una parte del posicionamiento SEO consiste en conseguir enlaces desde otras webs. Existen marketplaces donde se compran artículos patrocinados en medios y blogs. Cada plataforma publica su propio catálogo con métricas de autoridad (DA, DR, CF, TF), tráfico y precio, y un mismo medio puede aparecer en varias con precios distintos.

**Problema.** Comparar a mano esos catálogos es lento y poco reproducible. Además, las plataformas cambian su código con el tiempo y aparecen otras nuevas, por lo que el valor está en automatizar la captura y poder construir filtros y, a futuro, un histórico de precios.

**Contexto académico.** Trabajo Fin de Máster de 2023. El autor lo eligió en lugar de una de las propuestas estándar por dos motivos que cita la memoria: cubría casi todos los bloques del máster y servía de base para su web personal (blog y portfolio) con herramientas propias de SEO.

**Objetivos declarados en la memoria**

- Construir una aplicación web en Django con un blog (SEO, CRO, Python) y una sección de herramientas.
- Extraer datos de varias plataformas de venta de enlaces, empezando en notebooks y migrando el código a Django.
- Mostrar los datos al usuario registrado, con filtros por rango de tráfico y por DR, y permitirle guardar favoritos.
- Dejarlo preparado para escalar a más plataformas y comparar precios cuando haya enlaces comunes.

## Qué hace el proyecto

### Parte de investigación (notebooks)

Los notebooks de [`notebooks/`](notebooks/) prototiparon cada scraper con Selenium (login, paginación, extracción) antes de pasarlos a scripts. Los datos capturados están en `notebooks/data/` (CSV de Prensarank, Teblogueo, Conexoo y Publisuites, con varios miles de filas cada uno).

`Comparativa.ipynb` hace un cruce (`merge` externo por URL) de los CSV de Conexoo, Publisuites y Prensarank para ver el mismo medio en varias plataformas y resaltar el precio más bajo. Es un análisis exploratorio, no un estudio cerrado.

### Aplicación web (Django)

Módulos de la aplicación:

| Área | Estado |
|------|--------|
| Prensarank | Modelo, scraper y listado paginado (`/prensarank/`) conectados de extremo a extremo |
| Teblogueo | Modelo y scraper |
| Conexoo | Modelo y scraper |
| Blog | Apps `entrada` y `home`, edición con CKEditor, sitemap |
| Usuarios | Modelo de usuario propio (`applications/users`) |
| Favoritos | App `favoritos` para guardar medios |
| Publisuites, SEOlyze | Análisis en notebooks |

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
│   ├── scraperprensarank/   #   modelo + listado
│   ├── scraperteblogueo/    #   modelo
│   └── scraperconexoo/      #   modelo
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

Requiere Python 3.9, PostgreSQL y Chrome (para los scrapers).

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
DB_PASSWORD=change-me
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

En los notebooks, las credenciales de acceso aparecen como `***REDACTED***`.

## Estado del proyecto

Proyecto académico de 2023, publicado como muestra de trabajo. Las plataformas rastreadas pueden haber cambiado su interfaz desde entonces.

## Documentación

Memoria del trabajo: [`docs/TFM_FranciscoJavierLazaro.docx.pdf`](docs/TFM_FranciscoJavierLazaro.docx.pdf).

## Autor

Francisco Javier Lázaro. GitHub: [@pichu2707](https://github.com/pichu2707)

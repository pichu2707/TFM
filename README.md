# Webjavi: comparador de marketplaces de link building

Aplicación Django con scrapers Selenium que recopila y compara los catálogos de plataformas de compraventa de enlaces SEO (Prensarank, Teblogueo y Conexoo).

> Trabajo Fin de Máster (TFM), 2023. Memoria completa en [`docs/`](docs/TFM_FranciscoJavierLazaro.docx.pdf).

## Contexto

Quien compra enlaces (link building) debe elegir entre varios marketplaces, cada uno con su catálogo, sus métricas (DA, DR, tráfico, precio) y su propia interfaz. Comparar a mano es lento y poco reproducible.

Este proyecto automatiza la captura de esos catálogos, los guarda en una base de datos común, los expone en una web y los analiza en notebooks para comparar las plataformas con los mismos criterios.

## Funcionalidades

- Scrapers con Selenium para Prensarank, Teblogueo y Conexoo, con filtros configurables (idioma, categoría, país, tipo de enlace).
- Persistencia de los medios capturados mediante el ORM de Django.
- Web con listados por plataforma, blog (CKEditor), favoritos y usuarios propios.
- Notebooks de análisis comparativo, con CSV de resultados.

## Stack

| Área | Tecnología |
|------|------------|
| Backend | Django 4.2, django-ckeditor, django-environ, django-model-utils |
| Base de datos | PostgreSQL |
| Scraping | Selenium 4, webdriver-manager |
| Análisis | pandas, numpy, Jupyter |

## Estructura del proyecto

```text
.
├── manage.py
├── applications/        # Apps de Django
│   ├── home/            #   portada, contacto, sitemap
│   ├── users/           #   usuario personalizado
│   ├── entrada/         #   blog
│   ├── favoritos/       #   medios favoritos
│   ├── scraperprensarank/
│   ├── scraperteblogueo/
│   └── scraperconexoo/  #   modelos y vistas de cada plataforma
├── scrapers/            # Scripts Selenium (escriben en la BD vía ORM)
├── webjavi/             # Proyecto Django (urls, wsgi, settings/)
├── templates/  static/  media/
├── notebooks/           # Análisis comparativo
│   └── data/            #   CSV de resultados
├── docs/                # Memoria del TFM (PDF)
├── .env.example         # Variables de entorno de Django
├── config.example.json  # Credenciales y filtros de los scrapers
└── requirements.txt
```

## Arquitectura

1. Los scripts de `scrapers/` inician sesión en cada plataforma con Selenium, recorren el catálogo y normalizan los datos.
2. Cada script inicializa Django (`django.setup()`) y guarda los resultados en los modelos de `applications/scraper*`.
3. La web de Django lee esos modelos y muestra los listados por plataforma.
4. Los notebooks de `notebooks/` trabajan sobre los datos capturados (CSV) para la comparativa de la memoria.

## Inicio rápido

Requiere Python 3.9 o superior y Chrome instalado (para los scrapers).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env                  # editar SECRET_KEY
cp config.example.json config.json    # solo para los scrapers

createdb webjavi                      # o el nombre indicado en DB_NAME
python manage.py migrate
python manage.py runserver
```

Requiere una base de datos PostgreSQL accesible con los datos `DB_*` de `.env`. Varios modelos usan `CharField` sin `max_length`, algo que el backend de SQLite no admite al migrar.

Para ejecutar un scraper, desde la raíz del repositorio y con `config.json` completo:

```bash
python -m scrapers.prensarank
python -m scrapers.teblogueo
python -m scrapers.conexoo
```

## Notebooks

Los notebooks de [`notebooks/`](notebooks/) analizan cada plataforma (Prensarank, Teblogueo, Conexoo, Publisuites, SEOlyze) y las comparan en `Comparativa.ipynb`. Los CSV de entrada y salida están en `notebooks/data/`.

```bash
pip install -r requirements-notebooks.txt
jupyter notebook notebooks/
```

Las credenciales que aparecían en los notebooks originales fueron sustituidas por `***REDACTED***`.

## Documentación

La memoria del trabajo está en [`docs/TFM_FranciscoJavierLazaro.docx.pdf`](docs/TFM_FranciscoJavierLazaro.docx.pdf).

## Estado del proyecto

Proyecto académico de 2023, publicado como muestra de trabajo. Las plataformas rastreadas pueden haber cambiado su interfaz, por lo que los selectores de los scrapers podrían no funcionar hoy. No se mantiene activamente.

## Autor

Francisco Javier Lázaro, GitHub: [@pichu2707](https://github.com/pichu2707)

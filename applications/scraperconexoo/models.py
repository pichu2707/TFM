from django.db import models
from .managers import EntryScraper

# Create your models here.

class scraperConexoo(models.Model):
    # id = models.CharField('id',
    #                        max_length=50,
    #                        )
    
    url = models.CharField('url',
                            max_length=50,
                           )
    
    url_link = models.CharField('url_link',
                                max_length=75,
                                )
    
    descripcion = models.CharField('descripcion',
                                   )
    
    idioma = models.CharField('idioma',
                              max_length=10,
                              )
    
    pais_audiencia = models.CharField('pais_audiencia',
                                      max_length=10,
                                      )
    da = models.IntegerField(
                            'DA',
                            null=True,
                             )
    
    precio_post = models.CharField(
                                    'precio',
                                    max_length=10,
                                      )
    
    precio_post_cliente = models.CharField('precio_post_cliente',
                                            default=0,
                                            max_length=10,)
    
    max_links_post = models.CharField('max_links_post',
                                      null=True,
                                      max_length=3
                                      )
    
    tipo_sitio = models.CharField(
                                    'tipo',
                                    max_length=15,
                                  )
    
    tipo_sitio_text = models.CharField(
                                        'tipo_sitio_text',
                                        null=True,
                                        )
    
    traffic_organic = models.FloatField('trafico',
                                            )
    
    clase_web_text = models.CharField('clase',
                                    null=True,
                                    max_length=15,
                                    
                                 )
    
    tematicas_no_aceptadas_arr = models.CharField('tematicas_prohibidas',
                                                  )
    objects = EntryScraper()

    class Meta:
        verbose_name = 'Conexoo'
        verbose_name_plural = 'Conexoos'
        # constraint = [
        #     models.UniqueConstraint(fields=['url'], name='constraint_unico_url')
        # ]
    
    def __str__(self):
        return self.url+'-'+self.pais_audiencia+'-'+str(self.precio_post)
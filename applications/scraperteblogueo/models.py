from django.db import models

# from .managers import EntryScraper

class ScraperTeblogueo(models.Model):

    name = models.CharField(
            'name',
            # default='Sin Nombre'
    )
    url = models.CharField(
        'url',
        # blank=True
    )
    
    trust_flow = models.FloatField(
        'Trust Flow',
        null=True,
        blank=True
    )

    visits_month = models.FloatField(
        'visits_month',
        null=True,
        blank=True
    )

    peffer_pvp = models.FloatField(
        'peffer_pvp'
    )
    ppvp = models.FloatField(
        'ppvp'
    )
    max_links = models.FloatField(
        'max_links',
        null=True,
        default=0
    )
    sponsored_mark = models.BooleanField(
        'sponsored_mark'
    )
    model = models.CharField(
        'model'
    )

    #Crear columna linktype

    class Meta:
        verbose_name = 'Teblogueo'
        verbose_name_plural = 'Area Teblogueo'

    def __str__(self):
        return self.url+'-'+str(self.ppvp)
    

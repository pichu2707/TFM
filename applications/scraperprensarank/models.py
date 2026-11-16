from django.db import models

from .managers import EntryScraper
# Create your models here.


class ScraperPrensarank(models.Model):
    
    name = models.CharField(
            'Nombre',
            max_length=100,
    )
    url = models.CharField(
            'URL',
            max_length=50,
            #unique=True,
    )
    country = models.CharField(
        'País',
        max_length=25,
        default="sin país",
    )
    tipo = models.CharField(
        'Tipo',
        max_length=15,
        default='web',
        )
    dr = models.CharField(
            'DR',
            max_length=3
    ) 
    da = models.CharField(
            'DA',
            max_length=3,
    ) 
    cf = models.CharField(
            'CF',
            max_length=3,
            )
    tf = models.CharField(
            'TF',
            max_length=3
    ) 
    traffic = models.CharField(
            'Tráfico',
            max_length=9,
    ) 
    price = models.CharField(
            'Precio',
            max_length=7,
    ) 
    max_links = models.CharField(
            'Links máximos',
            max_length=6
    ) 
    max_links_groups = models.CharField(
            'Links Máximos de grupos',
            max_length=6
    )

    objects = EntryScraper() 

    class Meta:
        verbose_name = 'Prensarank'
        verbose_name_plural = 'Prensaranks'
        constraints = [
            models.UniqueConstraint(fields=['url'], name='constraint_unico_url')
        ]
    


    def __str__(self):
        return self.name+'-'+self.country+'-'+str(self.price)
    




    
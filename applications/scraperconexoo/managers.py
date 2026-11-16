from django.db import models

class EntryScraper(models.Manager):
    #Procedimiento para entradas

    def buscar_web(self, kword, country):
        #Búsqieda de entradas por url o precio
        if len(country) > 0:
            return self.filter(
                category_short_name=country,
                title_incontains=kword,
                public=True
            ).order_by('-created')
        else:
            return self.filter(
                title_incontains=kword,
                public=True
            ).order_by('-created')
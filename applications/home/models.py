from django.db import models

#apps de terceros
from model_utils.models import TimeStampedModel

# Create your models here.
class Home(TimeStampedModel):
    title = models.CharField(
        'Titulo',
        max_length=50
    )
    description = models.TextField()
    about_title = models.CharField(
        'Titulo Nosotros',
        max_length=50
    )

    about_text = models.TextField()
    about_email = models.EmailField(
        'email de contacto',
        max_length=254
    )
    
    class Meta:
        verbose_name = 'Pagina principal'
        verbose_name_plural = 'Paginas pricipales'

    def __str__(self):
        return self.title
    
class Suscribers(TimeStampedModel):
    # Suscripciones
    email = models.EmailField()

    class Meta:
        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'

    def __str__(self):
        return self.email
    
class Contact(TimeStampedModel):
    #Contactos
    full_name = models.CharField(
        'Nombres',
        max_length=60
    )

    email = models.EmailField()
    messagge = models.TextField()

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Mensajes'

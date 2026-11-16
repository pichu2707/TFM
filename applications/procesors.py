from applications.home.models import Home

#Procesor para recuperar teléfono y correo del registro home

def home_contact(request):
    home = Home.objects.latest('created')

    return {
        'correo':home.about_email,
    }
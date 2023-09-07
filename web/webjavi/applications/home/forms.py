from django import forms

#models
from .models import Suscribers, Contact

class SuscribersForm(forms.ModelForm):
    class Meta:
        model=Suscribers
        fields = (
            'email',
        )
        widgets = {
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'Email'
                }
            )
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact 
        fields=('__all__')
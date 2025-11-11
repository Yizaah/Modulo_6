from django import forms
from django.utils import timezone
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nombre', 'fecha', 'ubicacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha <= timezone.localdate():
            raise forms.ValidationError('La fecha del evento debe ser futura.')
        return fecha

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if nombre and len(nombre) > 100:
            raise forms.ValidationError('El nombre no debe superar los 100 caracteres.')
        return nombre



class ParticipantForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre del Participante')
    correo = forms.EmailField(label='Correo Electrónico')

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if not nombre:
            raise forms.ValidationError('El nombre del participante es obligatorio.')
        if len(nombre) > 100:
            raise forms.ValidationError('El nombre del participante no debe superar los 100 caracteres.')
        return nombre

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo:
            raise forms.ValidationError('El correo electrónico es obligatorio.')
        return correo

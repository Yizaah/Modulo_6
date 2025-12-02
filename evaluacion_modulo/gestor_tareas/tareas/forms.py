from django import forms

class TareaForm(forms.Form):
    titulo = forms.CharField(
        max_length=100,
        label="Título",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

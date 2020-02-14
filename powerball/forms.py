from django import forms
from .models import Picture


Class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        exclude = []

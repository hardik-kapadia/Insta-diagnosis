
from django import forms

DISEASES = [('covid', 'Covid-19'), ('brain_tumor', 'Brain Tumor')]


class ImageForm(forms.Form):
    image = forms.ImageField()
    disease = forms.ChoiceField(choices=DISEASES)

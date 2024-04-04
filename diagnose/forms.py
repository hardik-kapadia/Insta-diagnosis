
from django import forms

DISEASES = [('covid', 'Covid-19'), ('brain_tumor', 'Brain Tumor'),('arthritis','Knee Arthritis'),('kidney','Kidney stone')]


class ImageForm(forms.Form):
    image = forms.ImageField()
    disease = forms.ChoiceField(choices=DISEASES)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
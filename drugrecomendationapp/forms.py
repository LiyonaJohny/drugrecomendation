from django import forms
from django.forms import CharField
from drugrecomendationapp.models import mmodel

class mform(forms.Form):
    image=forms.FileField()
    class Meta:
        model=mmodel
        fields=['name','used','mg','dosage','cmp','effects','pres','pack','image']

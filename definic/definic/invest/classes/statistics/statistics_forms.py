from django import forms

class DescriptiveForm(forms.Form):
    pStock_code = forms.CharField()

class LinearGraphForm(forms.Form):
    pStock_code = forms.CharField()

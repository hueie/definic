from django import forms

class DataUpdateForm(forms.Form):
    pStockcode = forms.CharField()
    pStart = forms.CharField()
    pEnd = forms.CharField()
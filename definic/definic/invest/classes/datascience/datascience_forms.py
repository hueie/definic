from django import forms

class RegressionForm(forms.Form):
    pStockcode = forms.CharField()

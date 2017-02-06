from django import forms

class RegressionForm(forms.Form):
    pStock_code = forms.CharField()


class PreprocessorForm(forms.Form):
    pStock_code = forms.CharField()
    pSplit_ratio = forms.FloatField()
    
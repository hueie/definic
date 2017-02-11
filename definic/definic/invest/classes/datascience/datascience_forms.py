from django import forms

class NeuralnetworkForm(forms.Form):
    pStock_code = forms.CharField()

class RegressionForm(forms.Form):
    pStock_code = forms.CharField()


class PreprocessorForm(forms.Form):
    pStock_code = forms.CharField()
    pSplit_ratio = forms.FloatField()
    
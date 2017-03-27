from django import forms

class insertInventoryToDBForm(forms.Form):
    pIn_out = forms.CharField()
    pFrom_to = forms.CharField()
    pItem_id = forms.CharField()
    pExpense = forms.CharField()
    pQuantity = forms.CharField()
    pDate = forms.CharField()
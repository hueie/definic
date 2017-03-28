from django import forms

class insertInventoryToDBForm(forms.Form):
    pIn_out = forms.CharField()
    pFrom_to = forms.CharField()
    pItem_id = forms.CharField()
    pExpense = forms.CharField()
    pQuantity = forms.CharField()
    pDate = forms.CharField(required=False)
    
class insertTransactionToDBForm(forms.Form):
    pTr_id = forms.CharField(required=False)
    pPos_num = forms.CharField(required=False, initial="0")
    pItem_id = forms.CharField()
    pTr_price = forms.CharField(required=False, initial="0")
    pTr_quantity = forms.CharField(required=False, initial="0")
    pTr_Date = forms.CharField(required=False)
    
    def is_valid(self):
        valid = super(insertItemToDBForm, self).is_valid()
        for name in self.fields:
            if ( (self.cleaned_data[name] == None or self.cleaned_data[name] == '' or not self[name].html_name in self.data) and self.fields[name].initial is not None) :
                self.cleaned_data[name] = self.fields[name].initial
        return True
    
class insertItemToDBForm(forms.Form):
    pItem_id = forms.CharField(required=False)
    pItem_name = forms.CharField()
    pBarcode = forms.CharField(required=False, initial="0")
    pCur_price = forms.CharField(required=False, initial="0")
    pCur_quantity = forms.CharField(required=False, initial="0")
    pCur_place = forms.CharField(required=False)
    pItem_date = forms.CharField(required=False)
    
    def is_valid(self):
        valid = super(insertItemToDBForm, self).is_valid()
        for name in self.fields:
            if ( (self.cleaned_data[name] == None or self.cleaned_data[name] == '' or not self[name].html_name in self.data) and self.fields[name].initial is not None) :
                self.cleaned_data[name] = self.fields[name].initial
        return True
    
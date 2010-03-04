from django import forms
 
class RowInputForm(forms.Form):
    start = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'txtbox'}))
    end = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'txtbox'}))

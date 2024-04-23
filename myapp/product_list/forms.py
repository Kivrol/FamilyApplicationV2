from django import forms
from . import models
class AddProduct(forms.ModelForm):
    class Meta:
        model = models.ProductListComponent
        fields = ['name', 'unit', 'amount']

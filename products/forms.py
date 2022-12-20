
from django import forms
from .models import Product


# creating a form
class ProductForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = Product
        exclude = ["creator"]

        # specify fields to be used
        fields = [
            "productname",
            "price",
            "description",
            "photo",
        ]

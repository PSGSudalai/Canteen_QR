# BASE/forms.py

from django import forms
from BASE.models import CanteenItems


class CanteenItemForm(forms.ModelForm):
    class Meta:
        model = CanteenItems
        fields = ["identity", "price", "availability", "category"]

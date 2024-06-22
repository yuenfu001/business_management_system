from django import forms
from .models import Business, BusinessExpenditure, BusinessInflow,Transaction


class CreateBusiness(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"

class CreateBusinessExp(forms.ModelForm):
    class Meta:
        model = BusinessExpenditure
        fields = ["purchased_item", "purchased_quantity", "COG"]
        
class CreateBusinessInflow(forms.ModelForm):
    class Meta:
        model = BusinessInflow
        fields = ["sold_quantity", "COGS"]
        
        def clean_sold_quantity(self):
            sold_quantity = self.cleaned_data['sold_quantity']
            sold_item = self.instance.sold_item

            if sold_item and sold_quantity > sold_item.quantity_left:
                raise forms.ValidationError(f"Sold quantity exceeds available quantity left ({sold_item.quantity_left}).")
            return sold_quantity

class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["transaction"]
        

class CreateInventory(forms.ModelForm):
    class Meta:
        model = BusinessInflow
        fields = "__all__"

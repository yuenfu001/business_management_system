from django.contrib import admin
from .models import Business, Transaction,BusinessExpenditure, BusinessInflow
# Register your models here.

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date"]

@admin.register(BusinessExpenditure)
class BusinessExpenditureAdmin(admin.ModelAdmin):
 list_display = [
    "purchased_item", "purchased_quantity", "COG","total_amount"
 ]    

 @admin.register(BusinessInflow)
 class BusinessInflowAdmin(admin.ModelAdmin):
    list_display = [
       "get_purchased_item","sold_quantity","COGS","total_amount"
    ]

    def get_purchased_item(self,x):
       return x.sold_item.purchased_item
    
    get_purchased_item.short_description = "Purchased Item"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
   list_display = [
      "business_name","transaction","transaction_created"
   ]
    
  
 

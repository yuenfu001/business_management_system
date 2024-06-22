from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
# Create your models here

# Autogenerate transaction ID
def generate_transaction_id():
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d")
    latest_transaction = Transaction.objects.filter(transaction__startswith=f'TRANSACT-{date}-').order_by("-transaction").first()
    if latest_transaction:
        latest_number = int(latest_transaction.transaction.split("-")[-1])
        new_number = latest_number + 1
    else:
        new_number=1
    return f'TRANSACT-{date}-{new_number:04}'
    # abbreviation = business_name[:4].upper()
    # random_number = random.randint(10,99)

    # transaction_id = f'{abbreviation}-{date}-{random_number}'
    # return transaction_id
# Register A Business
class Business(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

# Register A Transaction
class Transaction(models.Model):
    business_name = models.ForeignKey(Business, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=50, unique=True, default=generate_transaction_id)
    transaction_created = models.DateField(auto_now=True)
    transaction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name}-{self.transaction}"
    
    # def save(self, *args, **kwargs):
    #     if not self.transaction:
    #         self.transaction = generate_transaction_id(self.business_name.name)
    #     super().save(*args, **kwargs)

# Register A Business Expenditure
class BusinessExpenditure(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    purchased_item = models.CharField(max_length=50)
    purchased_quantity = models.PositiveIntegerField(default=0)
    COG = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    total_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=40)
    quantity_left = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.transaction}{self.purchased_item}"
    

    def update_quantity_left(self):
        total_sold_quantity = self.ops.aggregate(sold_quantity= Sum('sold_quantity'))['sold_quantity'] or 0
        self.quantity_left = max(0, self.purchased_quantity - total_sold_quantity)
        self.save()

    def save(self, *args, **kwargs):
        self.total_amount = self.purchased_quantity * self.COG
        super().save(*args, **kwargs)

# Register A Business Inflow
class BusinessInflow(models.Model):
    sold_item = models.ForeignKey(BusinessExpenditure, on_delete=models.CASCADE, related_name="ops")
    sold_quantity = models.PositiveIntegerField(default=0)
    COGS = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    total_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=40)
    # quantity_left = models.PositiveIntegerField(default=0)
     
  
    
    # def save(self, *args, **kwargs):
    #     self.total_amount = self.sold_quantity * self.COGS
    #     if self.sold_quantity > self.sold_item.quantity_left:
    #         raise ValidationError(f"Can't sell more than {self.sold_item.quantity_left}")
    #     super().save(*args, **kwargs)
    #     self.sold_item.update_quantity_left()
    def clean(self):
        # Get the original sold_quantity
        original_quantity = 0
        if self.pk:
            original_quantity = BusinessInflow.objects.get(pk=self.pk).sold_quantity

        # Calculate the difference between the old and new sold_quantity
        quantity_difference = self.sold_quantity - original_quantity

        if quantity_difference > self.sold_item.quantity_left:
            raise ValidationError(f"Can't sell more than {self.sold_item.quantity_left} units.")
      
    def __str__(self):
        return f"{self.sold_item}{self.sold_quantity}"
    

        
    
# Register A stock Inventory
# class BusinessStock(models.Model):
#     purchased = models.ForeignKey(BusinessExpenditure, on_delete=models.CASCADE)
#     sold = models.ForeignKey(BusinessInflow, on_delete=models.CASCADE)
#     remaining = models.PositiveIntegerField(default=0)

#     def __str__(self) -> str:
#         return f'{self.purchased}'
    
#     def save(self, *args, **kwargs):
#         self.remaining = self.purchased.purchased_quantity - self.sold.sold_quantity
#         super().save(*args, **kwargs)
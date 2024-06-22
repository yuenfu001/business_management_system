from django.shortcuts import render,redirect,get_object_or_404
from .models import Business,Transaction ,BusinessExpenditure, BusinessInflow
from .forms import CreateBusiness, CreateBusinessExp, CreateBusinessInflow, CreateInventory,CreateTransactionForm
from django.contrib import messages
from django.core.exceptions import ValidationError
# Create your views here.

def home(request):
    All = Business.objects.all()
    context = {
        "all":All
    }
    return render(request,"base/index.html", context)

def createBusiness(request):
    All = Business.objects.all().order_by("-id")
    create_business = CreateBusiness(request.POST or None)
    if request.method == "POST":
        if create_business.is_valid():
            name = create_business.cleaned_data["name"]
            if All.filter(name=name).exists():
                return redirect("business:create")
                
            else:
                create_business.save()
                return redirect("business:create")
    context = {
        "create":create_business,
        "all":All,
    }
    return render(request, "create_business.html", context)

def transaction(request,pk):
    specific_business = get_object_or_404(Business, id=pk)
    get_transaction = Transaction.objects.filter(business_name=specific_business).order_by('-id')
    context = {
        "specific_business":specific_business,
        "all":get_transaction
    }
    return render(request,"transactions.html", context)
   
def createTransaction(request,pk):
    specific_business = get_object_or_404(Business, id=pk)
    create_transaction = CreateTransactionForm(request.POST or None)
    if request.method == "POST":
        if create_transaction.is_valid():
            form = create_transaction.save(commit=False)
            form.business_name = specific_business
            form.save()
            return redirect("business:get_transaction",pk=pk)
    
    context={
        "form":create_transaction
    }
    return render(request,"create_transaction.html",context)

def createExpenditure(request, pk):
    specific_transaction = get_object_or_404(Transaction,id=pk)
    expenditure = BusinessExpenditure.objects.filter(transaction=specific_transaction)
    create_expenditure = CreateBusinessExp(request.POST or None)
    if request.method =="POST":
        if create_expenditure.is_valid():
            form = create_expenditure.save(commit=False)
            form.transaction = specific_transaction
            form.save()
            return redirect("business:index")
    context = {
        "specific":specific_transaction,
        "get":expenditure,
        "expenditure":create_expenditure,
    }
    return render(request,"expenditure.html", context)

def viewExpenditure(request,pk):
    specific_transaction = get_object_or_404(Transaction,id=pk)
    expenditure = BusinessExpenditure.objects.filter(transaction=specific_transaction)
    context = {
        "specific":specific_transaction,
        "get":expenditure,

    }
    return render(request,"expenditure_details.html",context)

def createInflow(request,pk):
    specific_expenditure = get_object_or_404(BusinessExpenditure,id=pk)
    create_inflow = CreateBusinessInflow(request.POST or None)
    if request.method == "POST":
        if create_inflow.is_valid():
            try:
                form = create_inflow.save(commit=False)
                form.sold_item = specific_expenditure
                form.save()
                messages.success(request, "Business Inflow created successfully. ")
                return redirect("business:get_transaction",pk=pk)
            except ValidationError as e:
                create_inflow.add_error(None, e.message)
        else:
            messages.error(request, 'Sold Quantity is above Quantity Left')

    else:
        create_inflow = CreateBusinessInflow()
    context = {
        "expenditure":specific_expenditure,
        "form":create_inflow
    }
    return render(request,"create_inflow.html", context)

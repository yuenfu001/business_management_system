from django.urls import path
from . import views

app_name = "business"
urlpatterns = [
    path("", views.home, name="index"),
    path("create_business/", views.createBusiness, name="create"),
    path("create_expenditure/<str:pk>/", views.createExpenditure, name="create_expenditure"),
    path("view_expenditure/<str:pk>/", views.viewExpenditure, name="view_expenditure"),
    path("get_transaction/<str:pk>/", views.transaction, name="get_transaction"),
    path("create_transaction/<str:pk>/", views.createTransaction, name="create_transaction"),
    path("create_inflow/<str:pk>/", views.createInflow, name="create_inflow"),
]

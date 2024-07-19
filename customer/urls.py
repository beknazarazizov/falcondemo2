from django.urls import path

import customer.views.auth
from customer.views.auth import login_page, logout_page, register_page, SendEmailView
from customer.views.customers import CustomersTemplateView, AddCustomerTemplateView,DeleteCustomerView, EditCustomerView, export_data

urlpatterns = [
    path('customer-list/',CustomersTemplateView.as_view() , name='customers'),
    path('add-customer/', AddCustomerTemplateView.as_view(), name='add_customer'),
    path('customer/<int:pk>/',DeleteCustomerView.as_view(), name='delete'),
    path('customer/<int:pk>/update', EditCustomerView.as_view(), name='edit'),
    # Authentication path
    path('login-page/', login_page, name='login'),
    path('logout-page/',logout_page,name='logout'),
    path('register/',register_page,name='register'),
    path('export-data/', export_data, name='export_data'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),
    path('activate/<uidb64>/<token>/',customer.views.auth.activate, name='activate')

]

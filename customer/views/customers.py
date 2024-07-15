import csv
import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import TemplateView

from customer.forms import CustomerModelForm
from customer.models import Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# def customers(request):
#     customers = Customer.objects.all().order_by('id')
#     search_query = request.GET.get('search')
#     if search_query:
#         customers = Customer.objects.filter(
#             Q(full_name__icontains=search_query) | Q(address__icontains=search_query))
#
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(customers, 5)
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#
#     context = {
#         'page_obj': page_obj,
#         'search_query': search_query,
#         'customers': customers }
#     return render(request, 'customer/customer-list.html', context)

class CustomersTemplateView(TemplateView):
    template_name = 'customer/customer-list.html'

    def get_context_data(self, **kwargs):
        customer = Customer.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            customer = customer.filter(
                Q(name__icontains=search_query) | Q(billing_address__icontains=search_query)
            )

        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(customer, 5)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        context['customers'] = customer
        context['search_query'] = search_query
        return context



# def add_customer(request):
#     form = CustomerModelForm()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'customer/add-customer.html', context)
class AddCustomerTemplateView(TemplateView):
    template_name = 'customer/add-customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CustomerModelForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')


# def delete_customer(request, pk):
#     customer = Customer.objects.get(id=pk)
#     if customer:
#         customer.delete()
#         messages.add_message(
#             request,
#             messages.SUCCESS,
#             'Customer successfully deleted'
#         )
#         return redirect('customers')

class DeleteCustomerView(TemplateView):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=self.kwargs['pk'])
        customer.delete()
        return redirect("customers")


# def edit_customer(request, pk):
#     customer = Customer.objects.get(id=pk)
#     form = CustomerModelForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerModelForm(instance=customer, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#
#             return redirect('customers')
#     context = {
#         'form': form,
#     }
#     return render(request, 'customer/update-customer.html', context)

class EditCustomerView(TemplateView):
    template_name = 'customer/update-customer.html'

    def get_context_data(self, **kwargs):
        form = CustomerModelForm(instance=Customer.objects.get(id=self.kwargs['pk']))
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=self.kwargs['pk'])
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customers")

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return context


def export_data(request):
    format = request.GET.get('format', 'csv')
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=customers.csv'
        writer = csv.writer(response)
        writer.writerow(['Id', 'Full Name', 'Email', 'Phone Number', 'Address'])
        for customer in Customer.objects.all():
            writer.writerow([customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])


    elif format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customer.objects.all().values('full_name', 'email', 'phone_number', 'address'))
        # response.content = json.dumps(data, indent=4)
        response.write(json.dumps(data, indent=4))
        response['Content-Disposition'] = 'attachment; filename=customers.json'
    elif format == 'xlsx':
        pass

    else:
        response = HttpResponse(status=404)
        response.content = 'Bad request'

    return response
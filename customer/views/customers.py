from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from customer.forms import CustomerModelForm
from customer.models import Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def customers(request):
    search_query = request.GET.get('search')
    if search_query:
        customer_list = Customer.objects.filter(
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query))
    else:
        customer_list = Customer.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(customer_list, 10)
    try:
        paje_obj = paginator.page(page)
    except PageNotAnInteger:
        paje_obj = paginator.page(1)
    except EmptyPage:
        paje_obj = paginator.page(paginator.num_pages)


    context = {
        'paje_obj': paje_obj
    }
    return render(request, 'customer/customer-list.html', context)


def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {
        'form': form,
    }

    return render(request, 'customer/add-customer.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if customer:
        customer.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Customer successfully deleted'
        )
        return redirect('customers')


def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(instance=customer, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

            return redirect('customers')
    context = {
        'form': form,
    }
    return render(request, 'customer/update-customer.html', context)

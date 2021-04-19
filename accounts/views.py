from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm


# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()  # 客戶人數

    total_orders = orders.count()  # 訂單總數
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context=context)


def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context=context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()  # 返回與客戶有關的所有訂單，<QuerySet [<Order: Order object (1)>, <Order: Order object (3)>]>
    order_count = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count
    }
    return render(request, 'accounts/customer.html', context=context)


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Print POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}

    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)  # 訂單表單實例等於該訂單

    if request.method == 'POST':
        # print('Print POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

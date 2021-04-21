from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm  # 用戶創建的表格

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():  # 如果表單已驗證
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/originalRegister.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # 收到前端input
        password = request.POST.get('password')  # 收到前端input

        user = authenticate(request, username=username, password=password)  # 身份驗證

        if user is not None:  # 如果user存在登入
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=["customer"])
def userPage(request):
    orders = request.user.customer.order_set.all()
    print("Orders:", orders)

    total_orders = orders.count()  # 訂單總數
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/user.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["customer"])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/accounts_settings.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()  # 返回與客戶有關的所有訂單，<QuerySet [<Order: Order object (1)>, <Order: Order object (3)>]>
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):
    # https://docs.djangoproject.com/zh-hans/3.2/topics/forms/modelforms/#inline-formsets
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)  # 允許產品跟狀態
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})  # 讓他知道這個表單是誰的
    if request.method == 'POST':
        # print('Print POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():  # is_vaild : 建立在 form 底下的方法，可以用來驗證資料是否正確
            formset.save()
            return redirect("/")

    context = {'formset': formset}

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
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


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

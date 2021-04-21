from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  # 用戶創建的表格
from django.contrib.auth.models import User
from django import forms


from .models import Order, Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer  # model : 我要使用哪一個 Model
        fields = '__all__'  # fileds : 使用 Model 的哪些欄位
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
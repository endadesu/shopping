from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import ItemModel, CartModel, SalesModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.http import HttpResponse
import io
import matplotlib.pyplot as plt
import numpy as np


# Create your views here.
def indexfunc(request):
    return render(request, 'index.html')

def listfunc(request):
    item_list = ItemModel.objects.all()
    sort = sort_query(request)
    item_list = paginate_query(request, item_list, 9, sort)
    return render(request, 'list.html', {'item_list': item_list, 'sort':sort})

def loginfunc(request):
    if request.method == 'POST':
        wkUsername = request.POST['username']
        wkPassword = request.POST['password']
        user = authenticate(request, username=wkUsername, password=wkPassword)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')

def signupfunc(request):
    if request.method == 'POST':
        wkUsername = request.POST['username']
        wkPassword = request.POST['password']
        try:
            User.objects.get(username=wkUsername)
            return render(request, 'signup.html', {'error':'このユーザーは登録されています'})
        except:
            item_list = ItemModel.objects.all()
            user = User.objects.create_user(wkUsername, '',wkPassword)
            return render(request, 'list.html', {'item_list': item_list})
    return render(request, 'signup.html', {'some':'somedata'})

def cartfunc(request):
    id = request.user.id
    cart_list = CartModel.objects.filter(customerId=id)
    item_list = ItemModel.objects.all()
    stock = {}
    for citem in cart_list:
        stock[str(citem.itemId)] = item_list.filter(pk=citem.itemId)[0].stock
    return render(request, 'cart.html', {'cart_list':cart_list, 'stock':stock})

def addfunc(request):
    wk_customerId = request.user.id
    wk_itemId = request.POST['itemId']
    wkCartList = CartModel.objects.filter(customerId=wk_customerId, itemId=wk_itemId)
    wk_itemName = ItemModel.objects.get(pk = wk_itemId).name
    wk_itemValue = ItemModel.objects.get(pk = wk_itemId).value
    wk_numberOfItem = request.POST['numberOfItem']
    if wkCartList.count() > 0:
        sum = int(wkCartList[0].numberOfItem) + int(wk_numberOfItem)
        wkCartList.update(numberOfItem=sum)
    else:
        add_object = CartModel(customerId=wk_customerId, itemId=wk_itemId, itemName=wk_itemName, itemValue=wk_itemValue, numberOfItem=wk_numberOfItem)
        add_object.save()
    id = request.user.id
    cart_list = CartModel.objects.filter(customerId=id)
    item_list = ItemModel.objects.all()
    stock = {}
    for citem in cart_list:
        stock[str(citem.itemId)] = item_list.filter(pk=citem.itemId)[0].stock
    return render(request, 'cart.html', {'cart_list':cart_list, 'stock':stock})

def deletefunc(request, pk):
    CartModel.objects.filter(pk=pk).delete()
    id = request.user.id
    cart_list = CartModel.objects.filter(customerId=id)
    return render(request, 'cart.html', {'cart_list':cart_list})

def updatefunc(request):
    pk = request.POST['key']
    wk_numberOfItem = request.POST['numberOfItem']
    update_object = CartModel.objects.get(pk=pk)
    update_object.numberOfItem = wk_numberOfItem
    update_object.save()
    id = request.user.id
    cart_list = CartModel.objects.filter(customerId=id)
    return render(request, 'cart.html', {'cart_list':cart_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def deleteallfunc(request):
    id = request.user.id
    CartModel.objects.filter(customerId=id).delete()
    cart_list = CartModel.objects.filter(customerId=id)
    return render(request, 'cart.html', {'cart_list':cart_list})

def accountfunc(request):
    id = request.user.id
    cart_list = CartModel.objects.filter(customerId=id)
    item_list = ItemModel.objects.all()
    stockFlag = False
    name = ""
    for cartItem in cart_list:
        if cartItem.numberOfItem > ItemModel.objects.get(pk=cartItem.itemId).stock:
            stockFlag = True
            name = cartItem.itemName
            break
    
    if stockFlag:
        id = request.user.id
        cart_list = CartModel.objects.filter(customerId=id)
        item_list = ItemModel.objects.all()
        stock = {}
        for citem in cart_list:
            stock[str(citem.itemId)] = item_list.filter(pk=citem.itemId)[0].stock
        return render(request, 'cart.html', {'cart_list':cart_list, 'stock':stock, 'stockFlag': stockFlag, 'name': name})
    else:
        stock = {}
        for citem in cart_list:
            stock[str(citem.itemId)] = item_list.filter(pk=citem.itemId)[0].stock
        return render(request, 'account.html', {'cart_list':cart_list, 'stock':stock})
        

def endfunc(request):
    item_list = ItemModel.objects.all()
    id = request.user.id
    cart_list = CartModel.objects.filter(customerId=id)
    datetime_now = datetime.datetime.now().strftime('%Y%m%d')
    for item in cart_list:
        id = item.itemId
        val = ItemModel.objects.get(pk=id).value
        num = item.numberOfItem
        sum = val * num
        add_object = SalesModel(itemId=id, numberOfItem=num, sales=sum, date=datetime_now)
        add_object.save()

    for item in cart_list:
        wkItem = ItemModel.objects.get(pk=item.itemId)
        wkItem.stock = wkItem.stock - item.numberOfItem
        wkItem.save()

    id = request.user.id
    CartModel.objects.filter(customerId=request.user.id).delete()
    return render(request, 'end.html', {'somedate': 'somedate'})

def authorfunc(request):
    
    return render(request, 'author.html')

def authorAddfunc(request):
    wkPk = request.POST['pk']
    item = ItemModel.objects.get(pk=wkPk)

    
    wkName = request.POST['name']
    wkValue = request.POST['val']
    wkStock = request.POST['stock']
    
    try:
        wkImage = request.FILES['image']
        item.name = wkName
        item.value = wkValue
        item.stock = wkStock
        item.images = wkImage

        item.save()
    except:
        item.name = wkName
        item.value = wkValue
        item.stock = wkStock

        item.save()

    item_list = ItemModel.objects.all()
    return render(request, 'authorList.html', {'item_list': item_list})

def authorDeletefunc(request, pk):
    item = ItemModel.objects.get(pk=pk).delete()

    item_list = ItemModel.objects.all()
    return render(request, 'authorList.html', {'item_list': item_list})

def authorEditfunc(request, pk):
    item = ItemModel.objects.get(pk=pk)
    return render(request, 'authorEdit.html', {'item': item})

def authorListfunc(request):
    item_list = ItemModel.objects.all()
    sort = sort_query(request)
    item_list = paginate_query(request, item_list, 10, sort)
    return render(request, 'authorList.html', {'item_list': item_list, 'sort':sort})

def addItemfunc(request):
    if request.method == 'POST':
        wkName = request.POST['name']
        wkValue = request.POST['val']
        wkStock = request.POST['stock']
        wkImage = request.FILES['image']

        add_object = ItemModel(name=wkName, value=wkValue, stock=wkStock, images=wkImage)
        add_object.save()

        item_list = ItemModel.objects.all()
        return render(request, 'authorList.html', {'item_list': item_list})
    else:
        return render(request, 'addItem.html')

def paginate_query(request, queryset, count, sort):
    item_list = ItemModel.objects.all()
    if sort is not None:
        if sort == 'valAsc':
            item_list = ItemModel.objects.order_by('value')
        elif sort == 'valDesc':
            item_list = ItemModel.objects.order_by('value').reverse()
        elif sort == 'stockAsk':
            item_list = ItemModel.objects.order_by('stock')
        elif sort == 'stockDesc':
            item_list = ItemModel.objects.order_by('stock').reverse()
        elif sort == 'nameAsc':
            item_list = ItemModel.objects.order_by('name')
        elif sort == 'nameDesc':
            item_list = ItemModel.objects.order_by('name').reverse()
    paginator = Paginator(item_list, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginatot.page(paginator.num_pages)
    return page_obj

def sort_query(request):
    return request.GET.get('sort')

def salesfunc(request):
    sales_list = SalesModel.objects.all()
    return render(request, 'sales.html', {'sales_list': sales_list})

def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    buf.close()
    return s

def img_plot(request):
    sales_list = SalesModel.objects.order_by('date')
    allSales = {}
    for sales in sales_list:
        wkDate = sales.date
        wkSales = sales.sales
        if(wkDate in allSales):
            allSales[wkDate] = allSales[wkDate] + wkSales
        else:
            allSales[wkDate] = wkSales

    x = []
    y = []
    for date, sales in allSales.items():
        x.append(date)
        y.append(sales)
    
    plt.bar(x, y, align="center")
    plt.title("ALL SALES GRAPH")
    plt.xlabel("Date")
    plt.ylabel("Sales(yen)")
    plt.grid(True)
    png = plt2png()
    plt.cla()
    response = HttpResponse(png, content_type='image/png')
    return response
from django.contrib import admin
from django.urls import path, include
from .views import indexfunc, listfunc, loginfunc, signupfunc, cartfunc, addfunc, deletefunc, updatefunc, logoutfunc, deleteallfunc, accountfunc, endfunc, authorfunc, authorAddfunc, authorDeletefunc, authorEditfunc, authorListfunc, addItemfunc, salesfunc, img_plot

urlpatterns = [
    path('', indexfunc, name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('list/', listfunc, name='list'),
    path('login/', loginfunc, name='login'),
    path('signup/', signupfunc, name='signup'),
    path('cart/', cartfunc, name='cart'),
    path('add/', addfunc, name='add'),
    path('delete/<int:pk>/', deletefunc, name='delete'),
    path('update/', updatefunc, name='update'),
    path('logout/', logoutfunc, name='logout'),
    path('deleteall/', deleteallfunc, name='deleteall'),
    path('account/', accountfunc, name='account'),
    path('end/', endfunc, name='end'),
    path('author/', authorfunc, name='author'),
    path('authorAdd/', authorAddfunc, name='authorAdd'),
    path('authorDelete/<int:pk>/', authorDeletefunc, name='authorDelete'),
    path('authorEdit/<int:pk>/', authorEditfunc, name='authorEdit'),
    path('authorList/', authorListfunc, name='authorList'),
    path('addItem/', addItemfunc, name='addItem'),
    path('sales/', salesfunc, name='sales'),
    path('plot/', img_plot, name="img_plot"),
]

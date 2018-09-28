#from django.contrib import admin
from django.urls import path
from app_files import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),  
    path('show_dashboard', views.show_dashboard),
    path('logout',views.logout),
    path('add_thing_in_dashboard',views.add_thing_in_dashboard),
    #path('deleting_items_by_user', views.deleting_items_by_user),
    path('your_favorites/<int:quote_id>', views.your_favorites), 
    path('quotable_quotes/<int:quote_id>', views.quotable_quotes),
    path('user/<int:user_id>',views.userInfo)
]

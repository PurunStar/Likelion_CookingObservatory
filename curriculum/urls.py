from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    
    path('curi1/', views.curi1, name="curi1"),
    path('curr_landing_page/', views.curr_landing_page, name="curr_landing_page"),
    path('landing_page/', views.landing_page, name="landing_page"),
    path('lv1List/', views.lv1List, name="lv1List"),
    path('timer/', views.timer, name="timer"),

  
]
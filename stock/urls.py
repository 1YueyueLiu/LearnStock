from django.urls import path
from stock import views

app_name ='stock'

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
]
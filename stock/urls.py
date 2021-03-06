from django.urls import path
from stock import views


app_name ='stock'

urlpatterns = [
    path('stock/',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('add_category/',views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/',views.add_page,name='add_page'),
    #path('register/', views.register, name='register'),
    #path('login/',views.user_login, name='login'),
    path('restricted/',views.restricted,name='restricted'),
    #path('logout/',views.user_logout,name='logout'),
    path('goto/',views.goto_url, name='goto'),
    path('register_profile/',views.register_profile,name='register_profile'),
    path('News',views.News,name='News'),
    path('add_comment/<slug:category_name_slug>/', views.add_comment, name='add_comment'),
    path('search',views.search,name='search'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
]
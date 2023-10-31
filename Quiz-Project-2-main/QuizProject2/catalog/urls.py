from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('register/', views.new_page_view1, name='register'),
 path('log_in/', views.new_page_view2, name='new_page'),
 path('profile/<str:username>/', views.user_profile, name='user_profile')
]

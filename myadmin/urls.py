from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardPage),
    path('new-user/', views.UserCreatePage),
    path('users-table/',views.UserTablePage),
    path('user-remove/<int:id>/', views.DeleteUser, name="user_del"),
    path('user-edit/<int:id>/', views.EditUser, name="user_edit"),
    path('city-table/', views.CityTablePage),
    path('city-remove/<int:id>/', views.DeleteCity, name="city_del"),
    path('city-edit/<int:id>/', views.EditCity, name="city_edit"),
    
]

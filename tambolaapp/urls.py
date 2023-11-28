from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('page/<str:uid>/',views.PageView.as_view(),name="page"),
    path('RuleInGameFilter/<int:id>/',views.RuleInGameFilterView.as_view(),name="RuleInGameFilter"),
    path('AssignTo/<int:id>/',views.AssignToFilterView.as_view(),name="AssignTo"),
    path('JoinAGame/',views.JoinAGameFilterView.as_view(),name="JoinAGame"),
    path('Home/<int:id>/',views.HomeFilterView.as_view(),name="Home"),
    path('MyGame/<int:id>/',views.MyGameFilterView.as_view(),name="MyGame"),
    path('Compliment/<int:id>/',views.ComplimentFilterView.as_view(),name="Compliment"),
    path('Notification/<int:id>/',views.NotificationFilterView.as_view(),name="Notification"),






]
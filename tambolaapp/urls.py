
from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('RuleInGameFilter/<int:id>/',views.RuleInGameFilterView.as_view(),name="RuleInGameFilter"),
    path('page/<str:uid>/',views.PageView.as_view(),name="page"),
    path('buy-ticket-filter/<int:id>/',views.BuyTicketFilterView.as_view(),name="buy-ticket-filter"),
    path('wallet-amount/<int:id>/',views.GetWalletAmountView.as_view(),name="walletamt"),
    
    
]

"""
URL configuration for tambola project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from tambolaapp import views
from django.conf import settings  
from django.conf.urls.static import static

router = DefaultRouter()
router.register('User', views.UserView, basename='User'),
router.register('City', views.CityView, basename='City'),
router.register('Game_Rule', views.Game_RuleView, basename='Game_Rule'),
router.register('NewGame', views.NewGameView, basename='NewGame'),
router.register('RuleInGame', views.RuleInGameView, basename='RuleInGame'),
router.register('HelpAndSupport', views.HelpAndSupportView, basename='HelpAndSupport'),
router.register('AddMoney', views.AddMoneyView, basename='AddMoney'),
router.register('WalletAdd', views.WalletAddView, basename='WalletAdd'),
router.register('WalletAmt', views.WalletAmtView, basename='WalletAmt'),
router.register('PayByWalletAmount', views.PayByWalletAmountView, basename='PayByWalletAmount'),
router.register('Compliment', views.ComplimentView, basename='Compliment'),
router.register('ClaimRule', views.ClaimRuleView, basename='ClaimRule'),
router.register('Notification', views.NotificationView, basename='Notification'),
router.register('WithdrawRequest', views.WithdrawRequestView, basename='WithdrawRequest'),
router.register('BankDetail', views.BankDetailView, basename='BankDetail'),
router.register('buy-ticket', views.BuyTicketView, basename='buy-ticket'),
router.register('Ticket', views.TicketView, basename='Ticket'),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include("myadmin.urls")),
    path('', include(router.urls)),
    path('api/', include('tambolaapp.urls')),]


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
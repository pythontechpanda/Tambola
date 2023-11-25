from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.DashboardPage),
    path('', views.Login),
    # path('view-admin-profile/<int:id>/', views.ViewAdminProfile, name="admin_profile"),
    path('changepassword/<int:id>/',views.ForgotPassword, name='changepass'),
    path('logout/', views.logout_call, name='logout'),
    path('new-user/', views.UserCreatePage),
    path('users-table/',views.UserTablePage),
    path('user-remove/<int:id>/', views.DeleteUser, name="user_del"),
    path('user-edit/<int:id>/', views.EditUser, name="user_edit"),
    
    path('new-city/', views.CityCreate),
    path('city-table/', views.CityTablePage),
    path('city-remove/<int:id>/', views.DeleteCity, name="city_del"),
    path('city-edit/<int:id>/', views.EditCity, name="city_edit"),  
    
    path('new-game-rule/', views.GameRuleCreate),
    path('game-rule-table/', views.GameRuleTablePage),
    path('game-rule-remove/<int:id>/', views.DeleteGameRule, name="game_rule_del"),
    path('game-rule-edit/<int:id>/', views.EditGameRule, name="game_rule_edit"),  
    
    
    path('new-game/', views.NewGameCreate),
    path('new-game-table/', views.NewGameTablePage),
    path('new-game-remove/<int:id>/', views.DeleteNewGame, name="game_del"),
    path('new-game-edit/<int:id>/', views.EditNewGame, name="game_edit"), 
    path('game-view-detail/<int:id>/', views.DetailNewGame, name="view_detail"),
    
    path('rule-in-game/', views.RuleInGameCreate),
    path('rule-in-game-table/', views.RuleInGameTablePage),
    path('rule-in-game-remove/<int:id>/', views.DeleteRuleInGame, name="rule_in_game_del"),
    path('rule-in-game-edit/<int:id>/', views.EditRuleInGame, name="rule_in_game_edit"), 
    path('rule-in-game-view-detail/<int:id>/', views.DetailRuleInGame, name="view_detail_rule"),
    
    path('help-support-rule/', views.HelpAndSupportCreate),
    path('help-support-table/', views.HelpAndSupportTablePage),
    path('help-support-remove/<int:id>/', views.DeleteHelpAndSupport, name="help_del"),
    path('help-support-edit/<int:id>/', views.EditHelpAndSupport, name="help_edit"),  
    
    
    path('page-create/', views.PageCreate),
    path('page-table/', views.PageTablePage),
    path('page-remove/<int:id>/', views.DeletePage, name="page_del"),
    path('page-edit/<int:id>/', views.PageUpdate, name="page_edit"), 
    
    
    path('add-money-create/', views.AddMoneyCreate),
    path('add-money-table/', views.AddMoneyTablePage),
    path('add-money-remove/<int:id>/', views.DeleteAddMoney, name="money_del"),
    path('add-money-edit/<int:id>/', views.EditAddMoney, name="money_edit"),
    path('add-money-view-detail/<int:id>/', views.DetailAddMoney, name="view_money_detail"),
    
    
    path('wallet-add-create/', views.WalletAddCreate),
    path('wallet-add-table/', views.WalletAddTablePage),
    path('wallet-add-remove/<int:id>/', views.DeleteWalletAdd, name="wallet_del"),
    path('wallet-add-edit/<int:id>/', views.EditWalletAdd, name="wallet_edit"), 
    
    path('wallet-amount-create/', views.WalletAmtCreate),
    path('wallet-amount-table/', views.WalletAmtTablePage),
    path('wallet-amount-remove/<int:id>/', views.DeleteWalletAmt, name="wallet_amt_del"),
    path('wallet-amount-edit/<int:id>/', views.EditWalletAmt, name="wallet_amt_edit"),
    path('wallet-amount-view-detail/<int:id>/', views.DetailWalletAmt, name="view_money_detail"),
    
    
    path('pay-by-wallet-create/', views.PayByWalletAmountCreate),
    path('pay-by-wallet-table/', views.PayByWalletAmountTablePage),
    path('pay-by-wallet-remove/<int:id>/', views.DeletePayByWalletAmount, name="wallet_pay_del"),
    path('pay-by-wallet-edit/<int:id>/', views.EditPayByWalletAmount, name="wallet_pay_edit"),
    
    path('ticket-create/', views.TicketCreate),
    path('ticket-table/', views.TicketTablePage),
    path('ticket-remove/<int:id>/', views.DeleteTicket, name="ticket_del"),
    path('ticket-edit/<int:id>/', views.EditTicket, name="ticket_edit"),
    
    path('buy-ticket-create/', views.BuyTicketCreate),
    path('buy-ticket-table/', views.BuyTicketTablePage),
    path('buy-ticket-remove/<int:id>/', views.DeleteBuyTicket, name="buy_ticket_del"),
    path('buy-ticket-edit/<int:id>/', views.EditBuyTicket, name="buy_ticket_edit"), 
    path('buy-ticket-view-detail/<int:id>/', views.DetailBuyTicket, name="view_detail_buy_ticket"),
]

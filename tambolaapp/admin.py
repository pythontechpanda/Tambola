from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(City)
admin.site.register(Game_Rule)
admin.site.register(NewGame)
admin.site.register(RuleInGame)
admin.site.register(HelpAndSupport)
admin.site.register(Page)
admin.site.register(AddMoney)
admin.site.register(WalletAdd)
admin.site.register(WalletAmt)
admin.site.register(PayByWalletAmount)
admin.site.register(Ticket)
admin.site.register(BuyTicket)
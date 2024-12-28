from django.contrib import admin
from . models import UserLibraryAccount, UserAddress, DepositModel
# Register your models here.

admin.site.register(UserLibraryAccount)
admin.site.register(UserAddress)
# admin.site.register(DepositModel)

@admin.register(DepositModel)
class DepositAdmin(admin.ModelAdmin):
    list_display =['user', 'amount']
    
    def save_model(self, request, obj, form, change):
        obj.user.balance += obj.amount
        # send_transaction_mail(obj.account, obj.account.account_no, obj.amount ,"Loan Approval", "transactions/loan_approval.html")
        obj.user.save()
        
        super().save_model(request, obj, form, change)
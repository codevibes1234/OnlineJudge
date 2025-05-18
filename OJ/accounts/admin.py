from django.contrib import admin
import accounts.models
# Register your models here.
admin.site.register(accounts.models.OTP)
admin.site.register(accounts.models.ExtendedUser)
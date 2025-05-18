from django.urls import path
import accounts.views

urlpatterns = [
    path('register/',accounts.views.register,name='register-user'),
    path('login/',accounts.views.login_user,name='login'),
    path('logout/',accounts.views.logout_user,name='logout'),
    path('verify/<int:otpId>/<int:uId>/',accounts.views.verifyEmail,name='verify-email')
]

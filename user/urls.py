from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserReg.as_view(), name='UserReg'),
    path('login/', views.UserLogin.as_view(), name='UserLogin'),
    path('verify_user/', views.VerifyUser.as_view(), name='verify_user')
]

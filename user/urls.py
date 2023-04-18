from django.urls import path
from . import views


urlpatterns = [
    # path('user_reg/', views.user_reg, name='user_reg'),
    # path('user_login/', views.user_login, name='user_login'),
    path('user/', views.UserReg.as_view(), name='UserReg'),
    path('login/', views.UserLogin.as_view(), name='UserLogin')
]

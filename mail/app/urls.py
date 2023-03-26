from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),

    path("Registration/", Registration, name="Registration"),
    path("activate_email/<email_token>", activate_email, name="activate_email"),

    path("Login/", Login, name="Login"),
    path("LogOut/", LogOut, name="LogOut"),

    path("Cv_View/", Cv_View, name="Cv_View"),
    path("UserProfile/", UserProfile, name="UserProfile"),

    path("forget_password/", forget_password, name="forget_password"),
    path("Enter_otp/", Enter_otp, name="Enter_otp"),
    path("password_reset/", password_reset, name="password_reset"),
    #
    # path("send_mail_after_reg/", send_mail_after_reg, name="send_mail_after_reg"),
    # path("verify/", verify, name="verify"),
    #
    #
    # path('forget_password/', forget_password, name="forget_password"),
    #path('send_otp/<int: otp>', send_otp, name="send_otp"),
    #path('enter_otp/<int: otp>', enter_otp, name="enter_otp"),
    #path('Password_reset/<int: otp>', Password_reset, name="Password_reset"),
    path('test/', test, name="test"),

]
from django.urls import path

from . import auth_views
from . import views

urlpatterns = [
    # Register & Login URLs
    path('register/', auth_views.register_page, name="register"),
    path('login/', auth_views.login_page, name="login"),
    path('logout/', auth_views.logout_page, name="logout"),


    # Verification URLs
    path('verify_email/<str:auth_token>/', auth_views.verify_email_page, name="verify_email"),
    path('verify_phone/<str:auth_token>/', auth_views.verify_phone_page, name="verify_phone"),
    path('error/', auth_views.error, name="error"),
    path('change_password/<str:email>/<str:auth_token>/', auth_views.change_password, name="change_password"),
    path('forgot_password/', auth_views.forgot_password, name="forgot_password"),
    # path('check_email/', auth_views.check_your_email, name="error"),

]

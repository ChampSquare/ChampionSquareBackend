from django.urls import path
from . import views

app_name="Unicorn"

urlpatterns = [
    path('', views.home, name='home'),
    path('seeresult/', views.see_result, name="see_result"),
    path('login/', views.get_user_detail, name="login"),
    path('verification/', views.token_validation, name='token_validation'),  # noqa: E501

    # path('login/', views.login),
    path('ajax/contact/', views.contact, name='contact')

]

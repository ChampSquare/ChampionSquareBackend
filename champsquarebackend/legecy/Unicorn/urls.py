from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^seeresult/$', views.see_result, name="see_result"),
    url(r'^login/$', views.get_user_detail, name="login"),
    url(r'^verification/$', views.token_validation, name='token_validation'),  # noqa: E501

    # url(r'^login/', views.login),
    url(r'^ajax/contact/', views.contact, name='contact'),

]

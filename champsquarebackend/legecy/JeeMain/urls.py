from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/(?P<questionpaper_id>\d+)/$', views.show_exam_login_screen, name='login'),
    url(r'^instruction/(?P<questionpaper_id>\d+)/$', views.show_instruction, name='instruction'),

    url(r'^ajax/save_result/', views.save_exam_result, name='save_result'),
    url(r'^ajax/save_answer/', views.save_answer, name='save_answer'),
    url(r'^ajax/clear_answer/', views.clear_answer, name='clear_answer'),
    url(r'^ajax/save_unanswered/', views.save_unanswered, name='save_unanswered'),
    url(r'^ajax/save_answered/', views.save_answer, name='save_answer'),
    url(r'ajax/save_instruction_read/', views.save_instruction_state, name='save_instruction_state')

]
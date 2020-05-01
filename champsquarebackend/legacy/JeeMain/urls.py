from django.urls import path
from . import views

app_name="JeeMain"

urlpatterns = [
    path('login/<int:questionpaper_id>/', views.show_exam_login_screen, name='login'),
    path('instruction/<int:questionpaper_id>/', views.show_instruction, name='instruction'),

    path('ajax/save_result/', views.save_exam_result, name='save_result'),
    path('ajax/save_answer/', views.save_answer, name='save_answer'),
    path('ajax/clear_answer/', views.clear_answer, name='clear_answer'),
    path('ajax/save_unanswered/', views.save_unanswered, name='save_unanswered'),
    path('ajax/save_answered/', views.save_answer, name='save_answer'),
    path('ajax/save_instruction_read/', views.save_instruction_state, name='save_instruction_state')

]
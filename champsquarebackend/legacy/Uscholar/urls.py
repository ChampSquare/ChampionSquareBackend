from django.urls import path
from . import views

app_name = "Uscholar"

urlpatterns = [
    path('manage/add_question/', views.add_or_edit_question, name="add_question"),
    path('manage/add_question/<int:question_id>/', views.add_or_edit_question, name="edit_question"),
    path('manage/show_questions/', views.show_questions, name='show_questions'),
    path('manage/add_subject/', views.add_or_edit_subject, name='add_subject'),
    path('manage/add_subject/<int:subject_id>', views.add_or_edit_subject, name="edit_subject"),

]

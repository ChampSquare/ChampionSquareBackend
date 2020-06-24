from django.urls import path

from .question.views import question_list_view

app_name = "dashboard"

urlpatterns = [
    path('list_questions/', question_list_view, name="list_questions")
]
from django.urls import path

from .question import views

app_name = "dashboard"

urlpatterns = [
    path('list_questions/', views.QuestionListView.as_view(), name='list_questions'),
    path('questions/create/', views.QuestionCreateUpdateView.as_view(), name='create_question'),
    path('questions/<int:pk>/', views.QuestionCreateUpdateView.as_view(), name='update_question')
]
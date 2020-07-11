from rest_framework import serializers

from champsquarebackend.core.loading import get_model
from champsquarebackend.core.compat import get_user_model

Quiz = get_model('quiz', 'quiz')
QuestionPaper = get_model('quiz', 'Questionpaper')
User = get_user_model()



class QuizSerializer(serializers.ModelDurationField):
    users = serializers.PrimaryKeyRelatedField(
                many=True, allow_null=True)
    
    class Meta:
        model = Quiz
        fields = []

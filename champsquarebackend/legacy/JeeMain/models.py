from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

from champsquarebackend.legacy.Uscholar.models import AnswerPaper, Question

# Create your models here.

User = get_user_model()



class Result(models.Model):
    """AnswerPaper of user, one paper for each test"""
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    answer_paper = models.ForeignKey(AnswerPaper, on_delete=models.CASCADE)
    num_attempt = models.IntegerField(default=0)
    num_correct = models.IntegerField(default=0)
    num_wrong = models.IntegerField(default=0)
    marks_obtained = models.IntegerField(default=0)
    # answer = models.ManyToManyField(UserAnswer)

    def __str__(self):
        u = self.user
        q = self.answer_paper.question_paper.quiz
        return u'Result of paper of {0} for quiz {1}' \
            .format(u.profile.student.name, q.description)

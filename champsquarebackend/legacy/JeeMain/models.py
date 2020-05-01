from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

from champsquarebackend.legacy.Uscholar.models import AnswerPaper, Question

# Create your models here.

User = get_user_model()


class UserAnswer(models.Model):
    """Answer submitted by user"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_num = models.IntegerField(default=0)
    user_answer = models.CharField(max_length=5)
    right_answer = models.CharField(max_length=5)

    def get_answer_status(self):
        return self.user_answer == self.right_answer

    def __str__(self):
        return self.user_answer


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

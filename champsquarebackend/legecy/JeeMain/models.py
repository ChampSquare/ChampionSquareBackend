from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from Uscholar.models import AnswerPaper
from Uscholar.models import Question

# Create your models here.


class UserAnswer(models.Model):
    """Answer submitted by user"""
    question = models.ForeignKey(Question)
    question_num = models.IntegerField(default=0)
    user_answer = models.CharField(max_length=5)
    right_answer = models.CharField(max_length=5)

    def get_answer_status(self):
        return self.user_answer == self.right_answer

    def __str__(self):
        return self.user_answer


class Result(models.Model):
    """AnswerPaper of user, one paper for each test"""
    user = models.ForeignKey(User)
    answer_paper = models.ForeignKey(AnswerPaper)
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

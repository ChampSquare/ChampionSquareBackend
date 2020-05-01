from __future__ import unicode_literals

from django.db import models

from import_export import resources


# Create your models here.


class OfflineExam(models.Model):
    batch = models.CharField(max_length=30, null=False, blank=False)
    date = models.CharField(max_length=20, null=False, blank=False)
    full_marks = models.IntegerField()


class Student(models.Model):
    roll_number = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    # father_name = models.CharField(max_length=50, null=True,blank=True)
    # batch = models.CharField(max_length=20,null=True,blank=True)
    # mobile_number = models.CharField(max_length=15, null=True, blank=True)
    # father_number = models.CharField(max_length=15, null=True, blank=True)


class OfflineResult(models.Model):
    offline_exam = models.ForeignKey(OfflineExam, on_delete=models.CASCADE)
    rank = models.IntegerField()
    uid = models.IntegerField()
    name = models.CharField(max_length=50)
    correct = models.IntegerField(blank=True, null=True)
    incorrect = models.IntegerField(blank=True, null=True)
    marks = models.IntegerField(blank=True, null=True)
    percentile = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)


class OfflineExamResult(models.Model):
    """ Model to store result of offline exam """
    roll_number = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    batch = models.CharField(max_length=40, null=True, blank=True)
    correct = models.CharField(max_length=30, null=True, blank=True)
    incorrect = models.CharField(max_length=30, null=True, blank=True)
    full_marks = models.IntegerField(default=80)
    date = models.CharField(max_length=20, null=True, blank=True)
    rank = models.CharField(max_length=5, null=True, blank=True)
    marks = models.CharField(max_length=5, null=True, blank=True)
    percentile = models.CharField(max_length=5, null=True, blank=True)


class OfflineExamResultResource(resources.ModelResource):

    class Meta:
        model = OfflineExamResult
        fields = ('roll_number', 'name', 'batch', 'correct', 'incorrect', 'marks', 'rank', 'id',)


class StudentRecordResource(resources.ModelResource):
    class Meta:
        model = Student



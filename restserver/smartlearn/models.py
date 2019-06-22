from django.db import models
from restserver.restserver.common_models import SmartLearnBaseMode
from restserver.quiz.models import Class
from restserver import constants
from django.contrib.auth.models import User
from restserver.wiki.models import Topic
from restserver.quiz.models import Question


class Interaction(SmartLearnBaseMode):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    duration = models.PositiveIntegerField()
    student_count = models.PositiveIntegerField()
    interaction_col = models.CharField(max_length=constants.MAX_LENGTH)
    topics = models.ManyToManyField(Topic)
    topic_status = models.CharField(max_length=constants.MAX_LENGTH)


class Schedule(SmartLearnBaseMode):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    lecture_slot = models.PositiveIntegerField()
    total_slots = models.PositiveIntegerField()


class Assignment(SmartLearnBaseMode):
    isProject = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question)


class UserAssignments(SmartLearnBaseMode):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment , on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    remarks = models.CharField(blank=True)
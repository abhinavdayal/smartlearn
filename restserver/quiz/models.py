from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from model_utils.models import TimeStampedModel

from restserver.constants import MAX_LENGTH, LEVEL_CHOICES, PRIORITISATION_CHOICES
from restserver.restserver.common_models import SmartLearnBaseMode
from django.contrib.auth.models import User
from restserver.wiki.models import Topic, Outcome
from restserver.smartlearn.models import Assignment


class QuestionType(SmartLearnBaseMode):
    title = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField(blank=True, null=True)


class Question(SmartLearnBaseMode):
    ASSESSMENT_TYPE_CHOICES = (
        ("formative", "Formative"),
        ("summative", "Summative"),
        ("work_integrated", "Work Integrated"),
        ("diagnostic", "Diagnostic"),
        ("dynamic", "Dynamic"),
        ("synoptic", "Synoptic"),
        ("criterion_referenced", "Criterion Referenced"),
        ("ipsative", "Ipsative"),
    )
    slug = models.CharField(max_length=MAX_LENGTH, primary_key=True)
    title = models.CharField(max_length=MAX_LENGTH)
    text = JSONField()
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    is_interview_question = models.BooleanField(default=False)
    score = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=MAX_LENGTH, choices=LEVEL_CHOICES)
    is_assessment_question = models.BooleanField(default=False)
    is_exam_question = models.BooleanField(default=False)
    assessment_type = models.CharField(max_length=MAX_LENGTH,choices=ASSESSMENT_TYPE_CHOICES)
    # forum


class Hint(SmartLearnBaseMode):
    description = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField()


class Quiz(SmartLearnBaseMode):
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    level = models.CharField(max_length=MAX_LENGTH, choices=LEVEL_CHOICES)
    question = models.ManyToManyField(Question)


class Class(SmartLearnBaseMode):
    title = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()
    interaction_count = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.PositiveIntegerField()
    frequency_duration = models.PositiveSmallIntegerField()
    number_of_working_days = models.PositiveSmallIntegerField()
    lectures_per_interaction = models.PositiveSmallIntegerField()
    quiz = models.ManyToManyField(Quiz, through="ClassQuiz", through_fields=("quiz", "_class"))
    class_teacher = models.ManyToManyField(User, through="ClassTeachers", through_fields=("teacher", "_class"))
    outcome = models.ManyToManyField(Outcome)
    assignments = models.ManyToManyField(Assignment)


class ClassTeachers(SmartLearnBaseMode):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)


class ClassStudents(SmartLearnBaseMode):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    presence_count = models.PositiveSmallIntegerField()
    questions_asked_count = models.PositiveSmallIntegerField()
    questions_answered_count = models.PositiveSmallIntegerField()
    good_questions_count = models.PositiveSmallIntegerField()
    good_answer_count = models.PositiveSmallIntegerField()


class ClassQuiz(SmartLearnBaseMode, TimeStampedModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    number_of_attempts = models.PositiveSmallIntegerField()
    max_score = models.FloatField()
    min_score = models.FloatField()
    standard_deviation = models.FloatField()
    average = models.FloatField()
    median = models.FloatField()
    formative = models.IntegerField(MinValueValidator(0), MaxValueValidator(10))
    test_confidence = models.CharField(max_length=MAX_LENGTH, choices=PRIORITISATION_CHOICES)
    shuffle = models.BooleanField(default=False)
    max_grade = models.FloatField()
    duration = models.PositiveIntegerField()
    negative_penalty = models.PositiveSmallIntegerField(default=0)
    hint_penalty = models.PositiveSmallIntegerField(default=0)


class QuizAttempt(SmartLearnBaseMode, TimeStampedModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_answered = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    score = models.FloatField()
    remarks = models.TextField()
    is_partial = models.BooleanField(default=True)



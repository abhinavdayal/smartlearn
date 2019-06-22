from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeFramedModel

from restserver.constants import MAX_LENGTH, LEVEL_CHOICES
from restserver.restserver.common_models import SmartLearnBaseMode


class OutcomeType(SmartLearnBaseMode):
    name = models.CharField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Outcome(SmartLearnBaseMode):
    title = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()
    type = models.ForeignKey(OutcomeType, on_delete=models.CASCADE)


class Topic(SmartLearnBaseMode):
    title = models.CharField(max_length=MAX_LENGTH)
    number_of_contents = models.PositiveIntegerField()
    number_of_content_types = models.PositiveIntegerField()
    users_seen = models.ManyToManyField(User, related_name="users_seen")
    users_finished = models.ManyToManyField(User, related_name="users_finished")
    parent_topic = models.ForeignKey("self", on_delete=models.CASCADE)
    questions_count = models.PositiveIntegerField()
    easy_questions_count = models.PositiveIntegerField()
    moderate_questions_count = models.PositiveIntegerField()
    advance_questions_count = models.PositiveIntegerField()
    level = models.CharField(max_length=MAX_LENGTH, choices=LEVEL_CHOICES)
    easy_content_count = models.PositiveIntegerField()
    moderate_content_count = models.PositiveIntegerField()
    advanced_content_count = models.PositiveIntegerField()
    outcome = models.ManyToManyField(Outcome)
    authors = models.ManyToManyField(User, related_name="authors")
    # field for forums


class ContentType(SmartLearnBaseMode):
    name = models.CharField(max_length=MAX_LENGTH)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Content(SmartLearnBaseMode):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=MAX_LENGTH)
    level = models.CharField(max_length=MAX_LENGTH, choices=LEVEL_CHOICES)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    average_read_time = models.PositiveIntegerField()
    is_archive = models.BooleanField(default=False)
    reads_count = models.PositiveIntegerField(default=0)
    content_text = JSONField()
    type = models.ForeignKey(ContentType, on_delete=models.SET_DEFAULT)
    attempts = models.ManyToManyField(User, through="ContentAttempt", through_fields=("user", "content"))


class ContentAttempt(SmartLearnBaseMode):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    date_read = models.DateTimeField()
    has_read = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(blank=True, null=True)
    liked = models.BooleanField(default=False)
    level = models.CharField(max_length=MAX_LENGTH, choices=LEVEL_CHOICES)


class TopicAttempt(SmartLearnBaseMode, TimeFramedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    contents_read_total = models.PositiveIntegerField(default=0)
    contents_read_easy = models.PositiveIntegerField(default=0)
    contents_read_moderate = models.PositiveIntegerField(default=0)
    contents_read_advanced = models.PositiveIntegerField(default=0)
    questions_answered_total = models.PositiveIntegerField(default=0)
    questions_answered_easy = models.PositiveIntegerField(default=0)
    questions_answered_moderate = models.PositiveIntegerField(default=0)
    questions_answered_advanced = models.PositiveIntegerField(default=0)

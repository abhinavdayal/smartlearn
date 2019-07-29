from django.contrib.auth.models import User
from django.db import models
from restserver.restserver.common_models import SmartLearnBaseMode
from django.contrib.postgres.fields import JSONField
from restserver import constants


class Forum(SmartLearnBaseMode):
    pass


class Post(SmartLearnBaseMode):
    #forum
    content = JSONField()
    post_type = models.CharField(max_length=constants.MAX_LENGTH)
    is_good = models.BooleanField(default=False)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey("self", null=True)


class Comments(SmartLearnBaseMode):
    content = JSONField()
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

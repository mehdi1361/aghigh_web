from django.db import models
from django.contrib.auth.models import User as DjangoUser


class UserBox(DjangoUser):
    full_name = models.CharField(max_length=80)
    user_type = models.CharField(max_length=10)
    user_level = models.CharField(max_length=100)
    school_name = models.CharField(max_length=50)
    token = models.CharField(max_length=350)
    gender = models.CharField(max_length=10, null=True, blank=True, default=None)
    api_user_id = models.PositiveIntegerField(null=True, blank=True, default=False)
    province_id = models.PositiveIntegerField(null=True, blank=True, default=False)
    school_id = models.PositiveIntegerField(null=True, blank=True, default=False)
    image = models.TextField(null=True, blank=True,)
    gender_select = models.CharField(max_length=20, null=True, blank=True,)
    role_select = models.CharField(max_length=20, null=True, blank=True,)

    def __str__(self):
        return self.user.username

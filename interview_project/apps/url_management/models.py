import uuid

from django.contrib.auth.models import User
from django.db import models


class RedirectRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    redirect_url = models.URLField()
    is_private = models.BooleanField(default=False)
    redirect_identifier = models.CharField(max_length=10, unique=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.redirect_identifier:
            self.redirect_identifier = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.redirect_identifier} -> {self.redirect_url}"

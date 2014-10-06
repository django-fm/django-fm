from django.conf import settings
from django.db import models


class Feedback(models.Model):

    url = models.URLField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    update_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.url

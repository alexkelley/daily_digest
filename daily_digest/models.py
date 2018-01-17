import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now


class Quote_Author(models.Model):
    author = models.CharField(max_length=200, null=True, blank=True)
    biography_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.author


class Quote(models.Model):
    quote_author_id = models.ForeignKey(Quote_Author, on_delete=models.CASCADE, default=0)
    quote_text = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    submitter = models.CharField(max_length=100, null=True, blank=True)
    date_last_served = models.DateTimeField('date last served', default=now, blank=True)
    times_served = models.PositiveSmallIntegerField(default=0)
    votes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.quote_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Exercise(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    demo_url = models.URLField(null=True, blank=True)
    date_last_served = models.DateTimeField(default=now, blank=True)
    times_served = models.PositiveSmallIntegerField(default=0)
    votes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

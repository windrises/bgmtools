from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(primary_key=True, max_length=30)
    id = models.IntegerField(default=0)
    nick_name = models.CharField(max_length=200, default='')
    signup_time = models.CharField(max_length=10, default='')
    avater = models.CharField(max_length=300, default='')
    ban = models.IntegerField(default=0)
    vote_ban = models.IntegerField(default=0)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    sub_cat = models.CharField(max_length=10)
    cnt = models.IntegerField(default=0)
    class Meta:
        unique_together = ('name', 'sub_cat')

class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    sub_cat = models.CharField(max_length=10)
    img = models.CharField(max_length=300)
    namechs = models.CharField(max_length=500)
    namejp = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    tip = models.CharField(max_length=500)
    cat = models.CharField(max_length=30)
    dateid = models.IntegerField(default=0)
    date = models.CharField(max_length=10)
    star = models.CharField(max_length=5)
    votes = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    platform = models.CharField(max_length=500, default='')
    country = models.CharField(max_length=50, default='')

class Comment(models.Model):
    user = models.ForeignKey(User)
    subject = models.ForeignKey(Subject)
    star = models.IntegerField(default=0)
    time = models.CharField(max_length=20)
    timeid = models.IntegerField(default=0)
    content = models.CharField(max_length=1000)
    class Meta:
        unique_together = ('user', 'subject')

class AverageScore(models.Model):
    timeid = models.IntegerField(default=0)
    timestr = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject)
    score = models.FloatField(default=0)
    imdb_score = models.FloatField(default=0)
    rank = models.IntegerField(default=0)
    people = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    class Meta:
        unique_together = ('timeid', 'subject')

class AllAverageScore(models.Model):
    timeid = models.IntegerField(default=0)
    sub_cat = models.CharField(max_length=10)
    score = models.FloatField(default=0)
    class Meta:
        unique_together = ('timeid', 'sub_cat')

class Cache(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=10000)

from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class User(models.Model):
    user_name = models.CharField(primary_key=True, max_length=30)
    id = models.IntegerField(default=0)
    nick_name = models.CharField(max_length=200, default='')
    signup_time = models.CharField(max_length=10, default='')
    avatar = models.CharField(max_length=300, default='')
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

class RcmdIndex(models.Model):
    user = models.ForeignKey(User, related_name='rcmd_index')
    rcmd = models.ForeignKey(Subject, related_name='rcmded_index')
    rating = models.FloatField(default=0)
    marked = models.IntegerField(default=0)
    class Meta:
        unique_together = ('user', 'rcmd')

class RcmdedList(models.Model):
    user = models.ForeignKey(User, related_name='rcmd_list')
    rcmd = models.ForeignKey(Subject, related_name='rcmded_list')
    date = models.DateField(default=timezone.now)
    type = models.IntegerField(default=0)
    marked = models.IntegerField(default=0)
    class Meta:
        unique_together = ('user', 'rcmd', 'date')

class RcmdItem(models.Model):
    subject = models.ForeignKey(Subject, related_name='rcmd_item')
    rcmd = models.ForeignKey(Subject, related_name='rcmded_item')
    weight = models.FloatField(default=0)
    class Meta:
        unique_together = ('subject', 'rcmd')

class RcmdSub(models.Model):
    subject = models.ForeignKey(Subject, related_name='rcmd_sub')
    rcmd = models.ForeignKey(Subject, related_name='rcmded_sub')
    similarity = models.FloatField(default=0)
    class Meta:
        unique_together = ('subject', 'rcmd')

class RcmdUser(models.Model):
    user = models.ForeignKey(User, related_name='rcmd_user')
    rcmd = models.ForeignKey(User, related_name='rcmded_user')
    similarity = models.FloatField(default=0)
    class Meta:
        unique_together = ('user', 'rcmd')

class Settings(models.Model):
    user = models.OneToOneField(User, unique=True)
    last_update = models.DateField(default=timezone.now)
    score_below = models.FloatField(default=7.0)
    score_above = models.FloatField(default=0)
    rank_below = models.IntegerField(default=0)
    rank_above = models.IntegerField(default=100)
    rating_below = models.IntegerField(default=51)
    rating_above = models.IntegerField(default=0)
    filter_tag = models.CharField(max_length=2000, default='')

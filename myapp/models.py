from django.db import models

# Create your models here.

class AnimeTag(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    cnt = models.IntegerField(default=0)

class Anime(models.Model):
    id = models.IntegerField(primary_key=True)
    img = models.CharField(max_length=300)
    namechs = models.CharField(max_length=500)
    namejp = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    tip = models.CharField(max_length=500)
    cat = models.CharField(max_length=30)
    date = models.IntegerField()
    time = models.CharField(max_length=10)
    star = models.CharField(max_length=5)
    votes = models.IntegerField()
    rank = models.IntegerField()
    tag = models.ManyToManyField(AnimeTag)

class BookTag(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    cnt = models.IntegerField(default=0)

class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    img = models.CharField(max_length=300)
    namechs = models.CharField(max_length=500)
    namejp = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    tip = models.CharField(max_length=500)
    cat = models.CharField(max_length=30)
    date = models.IntegerField()
    time = models.CharField(max_length=10)
    star = models.CharField(max_length=5)
    votes = models.IntegerField()
    rank = models.IntegerField()
    tag = models.ManyToManyField(BookTag)

class MusicTag(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    cnt = models.IntegerField(default=0)

class Music(models.Model):
    id = models.IntegerField(primary_key=True)
    img = models.CharField(max_length=300)
    namechs = models.CharField(max_length=500)
    namejp = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    tip = models.CharField(max_length=500)
    cat = models.CharField(max_length=30)
    date = models.IntegerField()
    time = models.CharField(max_length=10)
    star = models.CharField(max_length=5)
    votes = models.IntegerField()
    rank = models.IntegerField()
    tag = models.ManyToManyField(MusicTag)

class GameTag(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    cnt = models.IntegerField(default=0)

class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    img = models.CharField(max_length=300)
    namechs = models.CharField(max_length=500)
    namejp = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    tip = models.CharField(max_length=500)
    cat = models.CharField(max_length=30)
    date = models.IntegerField()
    time = models.CharField(max_length=10)
    star = models.CharField(max_length=5)
    votes = models.IntegerField()
    rank = models.IntegerField()
    tag = models.ManyToManyField(GameTag)
    platform = models.CharField(max_length=500)

class RealTag(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    cnt = models.IntegerField(default=0)

class Real(models.Model):
    id = models.IntegerField(primary_key=True)
    img = models.CharField(max_length=300)
    namechs = models.CharField(max_length=500)
    namejp = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    tip = models.CharField(max_length=500)
    cat = models.CharField(max_length=30)
    date = models.IntegerField()
    time = models.CharField(max_length=10)
    star = models.CharField(max_length=5)
    votes = models.IntegerField()
    rank = models.IntegerField()
    tag = models.ManyToManyField(RealTag)
    country = models.CharField(max_length=50)


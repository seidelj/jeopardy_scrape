from django.db import models

# Create your models here.

class AirDates(models.Model):
	airdate = models.CharField('Date Aired', max_length=256)
	game = models.IntegerField()
	contestants = models.ManyToManyField('Contestants')

class Documents(models.Model):
	clue = models.TextField('Clue')
	answer = models.CharField("Answer", max_length=256)
	right = models.CharField("Right", max_length=256)

class Categories(models.Model):
	category = models.CharField("Category", max_length=256)

class Clues(models.Model):
	c_game = models.ForeignKey(AirDates, blank=True, null=True)
	c_document = models.ForeignKey(Documents, blank=True, null=True)
	c_round = models.IntegerField()
	c_value = models.IntegerField() 

class Classifications(models.Model):
	clue_id = models.ForeignKey(Clues, blank=True, null=True)
	category_id = models.ForeignKey(Categories, blank=True, null=True)

class Contestants(models.Model):
	player_id = models.IntegerField('Player ID')
	player_name = models.CharField('Player Name', max_length=256)
	player_nickname = models.CharField('Nickname', max_length=256)

class Earnings(models.Model):
	round1 = models.IntegerField()
	round2 = models.IntegerField()
	round3 = models.IntegerField()
	e_game = models.ForeignKey(AirDates, blank=True, null=True)
	e_player = models.ForeignKey(Contestants, blank=True, null=True)

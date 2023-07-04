from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    emblem = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    shortName = models.CharField(max_length=255, null=True, blank=True)
    tla = models.CharField(max_length=255, null=True, blank=True)
    crest = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    utcDate = models.DateTimeField()
    status = models.CharField(max_length=255)
    minute = models.IntegerField(blank=True, null=True)
    injuryTime = models.IntegerField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    matchDay = models.IntegerField()
    stage = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    homeTeam = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    scoreHome = models.CharField(max_length=255, blank=True, null=True)
    scoreAway = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f'{self.homeTeam} vs {self.awayTeam}'

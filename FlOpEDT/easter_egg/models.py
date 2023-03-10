from django.db import models
from django.conf import settings

class GameScore(models.Model):
    score = models.PositiveIntegerField()
    user = models.OneToOneField('people.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.score}'

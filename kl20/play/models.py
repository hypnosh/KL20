from django.db import models

# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=150)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name - self.question}"

class Attempt(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    correct = models.BooleanField()
    user = models.ForeignKey(User)

    def __str__(self):
        return f"{self.user} - {self.level}"
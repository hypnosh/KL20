from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    last_level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

def upload_path(instance, filename):
        return f'{filename}'

class Level(models.Model):
    level_identifier = models.CharField(max_length=7, null=True)
    checkpoint = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True)
    image = models.ImageField(upload_to = upload_path,null=True)
    question = models.TextField()
    
    answer = models.CharField(max_length=50)
    routes = models.JSONField(null=True, blank=True)

    headcomment = models.CharField(max_length=100, null=True, blank=True)    
    sourcehint = models.TextField(null=True, blank=True)
    
    prev_level = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # list of tuples (answer, message)

    class AlignmentH(models.TextChoices):
        LEFT = 'left', 'Left'
        CENTER = 'hcenter', 'Center'
        RIGHT = 'right', 'Right'
    class AlignmentV(models.TextChoices):
        TOP = 'top', 'Top'
        CENTER = 'vcenter', 'Center'
        BOTTOM = 'bottom', 'Bottom'
    
    alignH = models.CharField(
        max_length=7, 
        default="hcenter",
        choices=AlignmentH.choices,
    )
    alignV = models.CharField(
        max_length=7, 
        default="vcenter",
        choices=AlignmentV.choices,
    )

    def __str__(self):
        return f"{self.level_identifier} - {self.name}"
    

class Attempt(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    correct = models.BooleanField()
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    answer = models.CharField(max_length=50, null=True, default="")

    def __str__(self):
        return f"{self.player} - {self.level}"
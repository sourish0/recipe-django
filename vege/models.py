from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recipe(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    recipe_image = models.ImageField(upload_to='recipe_images')
    recipe_view_count = models.IntegerField(default=1)
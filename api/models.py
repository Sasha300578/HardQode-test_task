from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products')
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    access_granted = models.DateTimeField(auto_now_add=True)

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField()

class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(User, related_name='enrolled_groups')  # Изменено здесь
    min_students = models.IntegerField()
    max_students = models.IntegerField()


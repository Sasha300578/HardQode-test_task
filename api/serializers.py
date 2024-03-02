from rest_framework import serializers
from .models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_datetime', 'cost', 'creator', 'lessons_count']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url']
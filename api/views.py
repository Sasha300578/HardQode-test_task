from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Lesson, Access, Group
from .serializers import ProductSerializer, LessonSerializer
from django.db import models
from .utils import distribute_user_to_group


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        if Access.objects.filter(user=user, product_id=product_id).exists():
            return Lesson.objects.filter(product_id=product_id)
        else:
            return Lesson.objects.none()

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.annotate(lessons_count=models.Count('lessons')).all()
    serializer_class = ProductSerializer

class AccessCreateView(APIView):
    def post(self, request, product_id):
        user = request.user  # Получаем пользователя из запроса
        product = get_object_or_404(Product, pk=product_id)  # Получаем продукт по ID

        # Создаем объект доступа
        access, created = Access.objects.get_or_create(user=user, product=product)
        if created:
            # Если доступ создан, распределяем пользователя по группе
            distribute_user_to_group(user, product)
            return Response({'status': 'access granted'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'access already exists'}, status=status.HTTP_200_OK)
from django.utils import timezone
from django.db import models


def distribute_user_to_group(user, product):
    # Проверка, начался ли продукт
    if product.start_datetime > timezone.now():
        # Продукт еще не начался, можно перераспределять группы
        groups = list(product.groups.annotate(count_students=models.Count('students')).order_by('count_students'))
        for group in groups:
            if group.students.count() < group.max_students:
                group.students.add(user)
                break
    else:
        # Продукт уже начался, распределяем по первой доступной группе
        group = product.groups.annotate(count_students=models.Count('students')).filter(count_students__lt=models.F('max_students')).first()
        if group:
            group.students.add(user)

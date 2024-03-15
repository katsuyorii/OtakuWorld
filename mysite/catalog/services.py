from .models import Comment, Product
from django.db.models import Avg

# Функция рассчета рейтинга для продукта
def rating_calculate(product):
    average_grade = Comment.objects.filter(product=product).aggregate(avg_grade=Avg('grade'))['avg_grade']

    select_product = Product.objects.get(slug=product.slug)
    select_product.rating = average_grade
    select_product.save()
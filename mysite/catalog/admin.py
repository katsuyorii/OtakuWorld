from django.contrib import admin
from .models import Category, Genre, Source, Product, Property, ProductProperty, Comment, Favorites

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Source)
admin.site.register(Product)
admin.site.register(Property)
admin.site.register(ProductProperty)
admin.site.register(Comment)
admin.site.register(Favorites)

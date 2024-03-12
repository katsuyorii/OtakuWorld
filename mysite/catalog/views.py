from django.views.generic.list import ListView
from .models import Category, Product, ProductProperty, Comment
from django.shortcuts import get_object_or_404

# Класс-представления каталога категорий
class CatalogView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории товаров'

        return context


# Класс-представление для каталога товаров
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product-list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        queryset = Product.objects.filter(category__slug=self.kwargs['category_slug']).select_related('category')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])

        return context
    

# Класс-представление для отдельного товара
class ProductDetailView(ListView):
    model = Product
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = {
            'base': get_object_or_404(Product.objects.select_related('category', 'source'), slug=self.kwargs['product_slug']),
            'characters': ProductProperty.objects.filter(product__slug=self.kwargs['product_slug']),
            'comments': Comment.objects.filter(product__slug=self.kwargs['product_slug']),
        }

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'

        return context
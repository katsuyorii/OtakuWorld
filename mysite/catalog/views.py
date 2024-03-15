from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Category, Product, ProductProperty, Comment
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from .forms import AddNewCommentForm
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser


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
class ProductDetailView(ListView, FormMixin):
    model = Product
    form_class = AddNewCommentForm
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = {
            'base': get_object_or_404(Product.objects.select_related('category', 'source'), slug=self.kwargs['product_slug']),
            'characters': ProductProperty.objects.filter(product__slug=self.kwargs['product_slug']).select_related('product', 'property'),
            'comments': Comment.objects.filter(product__slug=self.kwargs['product_slug']).select_related('user').order_by('-create_date'),
        }

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        context['count_reviews'] = Comment.objects.filter(product__slug = self.kwargs['product_slug']).count()

        # Проверка, если пользователь не авторизирован, то у него нет доступа к форме создания комментария
        if isinstance(self.request.user, AnonymousUser):
            context['user_comm'] = True
        else:
            context['user_comm'] = Comment.objects.filter(user=self.request.user, product__slug=self.kwargs['product_slug']).exists()

        return context
    
    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs = {'category_slug': self.kwargs['category_slug'], 'product_slug': self.kwargs['product_slug']})
    
    # Метод добавления комментариев
    def post(self, request, *args, **kwargs):
        # -------- НЕ ТРОГАТЬ -----------------
        self.object_list = self.get_queryset()
        # -------------------------------------

        form = self.get_form()
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = get_object_or_404(Product.objects.select_related('category', 'source'), slug=self.kwargs['product_slug'])
            new_comment.user = self.request.user
            new_comment.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        messages.info(self.request, 'Ваш комментарий успешно добавлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при заполнении формы!')
        return super().form_invalid(form)
    
    
    
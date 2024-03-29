from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from django.views.generic.edit import FormMixin

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.db import transaction
from .models import Category, Product, ProductProperty, Comment, Favorites, Genre, Source

from .forms import AddNewCommentForm, EditCommentForm

from django.shortcuts import get_object_or_404, redirect
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
        context['selected_category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['genres'] = Genre.objects.all()
        context['sources'] = Source.objects.all()

        return context
    

# Класс-представление для отдельного товара
class ProductDetailView(DetailView, FormMixin):
    model = Product
    form_class = AddNewCommentForm
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_queryset(self):
        queryset = Product.objects.filter(slug=self.kwargs['product_slug']).select_related('category', 'source')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['proretries'] = ProductProperty.objects.filter(product__slug=self.kwargs['product_slug']).select_related('property')
        context['comments'] = Comment.objects.filter(product__slug=self.kwargs['product_slug']).select_related('user').order_by('-create_date')
        context['count_reviews'] = Comment.objects.filter(product__slug = self.kwargs['product_slug']).count()

        # Проверка, если пользователь не авторизирован, то у него нет доступа к форме создания комментария и добавления в избранное
        if isinstance(self.request.user, AnonymousUser):
            context['is_user_comment'] = True
            context['is_favorites'] = False
        else:
            context['is_user_comment'] = Comment.objects.filter(user=self.request.user, product__slug=self.kwargs['product_slug']).exists()
            context['is_favorites'] = Favorites.objects.filter(user=self.request.user, product__slug = self.kwargs['product_slug']).exists()

        return context
    
    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs = {'category_slug': self.kwargs['category_slug'], 'product_slug': self.kwargs['product_slug']})
    
    # Метод добавления комментариев
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
            new_comment.user = self.request.user
            new_comment.save()
            new_comment.product.update_rating()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        messages.success(self.request, 'Ваш комментарий успешно добавлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при заполнении формы!')
        return super().form_invalid(form)


# Класс-представление для удаления комментария
class CommentDeleteView(View):
    @transaction.atomic()
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        comment.product.update_rating()

        messages.success(request, 'Ваш комментарий успешно удален!')

        return redirect(reverse_lazy('product_detail', kwargs = {'category_slug': comment.product.category.slug, 'product_slug': comment.product.slug}))
    

# Класс-представление для редактирования комментария
class CommentEditView(UpdateView):
    model = Comment
    form_class = EditCommentForm
    template_name = 'catalog/review-edit.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        queryset = Comment.objects.filter(pk=self.kwargs['comment_id']).select_related('product__category')

        return queryset

    @transaction.atomic()
    def form_valid(self, form):
        self.object = form.save()
        self.object.product.update_rating()
        
        messages.success(self.request, 'Ваш комментарий успешно редактирован!')
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при заполнении формы!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Редактирование комментария'

            return context

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs = {'category_slug': self.object.product.category.slug, 'product_slug': self.object.product.slug})


# Класс представление для добавления в избранное
class FavoritesAddUserView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])

        if not Favorites.objects.filter(product=product, user=request.user):
            new_favorite = Favorites(product=product, user=request.user)
            new_favorite.save()
            button_text = 'В избранном'
            button_color = 'red'
            new_img = '/static/img/icons/heart-red.png'
        else:
            selected_favorite = Favorites.objects.filter(product=product, user=request.user)
            selected_favorite.delete()
            button_text = 'В избранное'
            button_color = 'black'
            new_img = '/static/img/icons/icon-love.png'

        return JsonResponse({'button_text': button_text, 'button_color': button_color, 'new_img': new_img})
    

# Класс представление для динамической фильтрации
class DynamicFiltersProducts(View):
    def get(self, request, *args, **kwargs):
        selected_filters = request.GET
        
        filtered_products = Product.objects.filter(source__name=selected_filters)

        json_filtered_products = list(filtered_products)

        return JsonResponse({'products': json_filtered_products})
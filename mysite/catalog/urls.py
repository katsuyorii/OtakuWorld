from django.urls import path
from .views import CatalogView, ProductListView, ProductDetailView, CommentDeleteView, CommentEditView, FavoritesAddUserView, DynamicFiltersProducts
from django.contrib.auth.decorators import login_required
from .decorators import check_comment_user

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('dynamic-filters/', DynamicFiltersProducts.as_view(), name='dynamic-filters'),
    path('delete_comment/<int:comment_id>', check_comment_user(CommentDeleteView.as_view()), name='delete_comment'),
    path('edit_comment/<int:comment_id>', check_comment_user(CommentEditView.as_view()), name='edit_comment'),
    path('add_favorites/<int:product_id>', login_required(FavoritesAddUserView.as_view()), name='add_favorites'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list'),
]
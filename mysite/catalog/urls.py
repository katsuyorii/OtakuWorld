from django.urls import path
from .views import CatalogView, ProductListView, ProductDetailView, CommentDeleteView, CommentEditView

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('delete_comment/<int:comment_id>', CommentDeleteView.as_view(), name='delete_comment'),
    path('edit_comment/<int:comment_id>', CommentEditView.as_view(), name='edit_comment'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list'),
]
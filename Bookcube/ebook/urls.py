from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('read/<int:book_id>/', EbookReadView.as_view(), name='read_ebook'),
    path('order/', OrderView.as_view(), name='order'),
    path('search/', SearchView.as_view(), name='search'),
    path('store/', StoreView.as_view(), name='store'),
    path('serie/<int:series_id>/', SerieDetailView.as_view(), name='serie_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('manager_add_book/', AdminAddBookView.as_view(), name='admin_add_book'),
    path('manager_add_serie/', AdminAddSerieView.as_view(), name='admin_add_serie'),
    path('manager_add_author/', AdminAddAuthorView.as_view(), name='admin_add_author'),
    path('favorites/', FavoriteView.as_view(), name='favorites'),
    path('add_to_favorites/<int:series_id>/', AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('remove_from_favorites/<int:series_id>/', RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('checkout/', views.checkout, name='checkout'),
    path('book/<int:book_id>/reviews/', ReviewView.as_view(), name='reviews'),
    path('form_review/<int:book_id>/', FormReviewView.as_view(), name='form_review'),
    path('manage_books/', ManageBookView.as_view(), name='manage_book'),
    path('edit_book/<int:book_id>/', EditBookView.as_view(), name='admin_edit_book'),
    path('delete_book/<int:book_id>/', DeleteBookView.as_view(), name='delete_book'),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('read/<int:book_id>/', EbookReadView.as_view(), name='read_ebook'),
    path('order/', OrderView.as_view(), name='order'),
    path('search/', SearchView.as_view(), name='search'),
    path('store/', StoreView.as_view(), name='store'),
    path('serie/<int:series_id>/', SerieDetailView.as_view(), name='serie_detail'),
]

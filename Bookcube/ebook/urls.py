from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('read/<int:book_id>/', EbookReadView.as_view(), name='read_ebook'),
]

# Create your views here.
from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Avg


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        
        if request.user.is_authenticated:
            completed_order_items = OrderItem.objects.filter(order__user=request.user, order__status='Completed')
            context['completed_order_items'] = completed_order_items
            context['has_completed_orders'] = completed_order_items.exists()
        
        
        context['books'] = Book.objects.all()  
        return render(request, 'dashboard.html', context)

class EbookReadView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        return render(request, 'ebook.html', {'book': book})



class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        books = Book.objects.all()
        orders = Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.filter(order__user=request.user)
        book_prices = {book.id: book.price for book in books}
        return render(request, 'order.html', {'orders': orders, 'order_items': order_items, 'books': books, 'book_prices': book_prices})

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        books = Book.objects.filter(title__icontains=query)
        authors = Author.objects.filter(name__icontains=query)
        series = BookSeries.objects.all().annotate(average_rating=Avg('books__reviews__rating'))
        if query:
            series = series.filter(title__icontains=query)

        context = {
            'query': query,
            'books': books,
            'authors': authors,
            'series': series,
        }
        return render(request, 'search.html', context)
class StoreView(View):
    def get(self, request):
        context = {}
        books = Book.objects.all()
        context['books'] = books
        if request.user.is_authenticated:
            completed_order_items = OrderItem.objects.filter(order__user=request.user, order__status='Completed')
            context['completed_order_items'] = completed_order_items
            context['has_completed_orders'] = completed_order_items.exists()
        
        return render(request, 'store.html', context)

class SerieDetailView(View):
    def get(self, request, series_id):
        series = get_object_or_404(BookSeries, id=series_id)
        
        context = {
            'series': series,
        }
        return render(request, 'serie_detail.html', context)
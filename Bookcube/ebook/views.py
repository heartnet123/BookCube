# Create your views here.
from django.shortcuts import redirect, render
from .models import *
from django.views.generic import TemplateView
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.db.models import Avg
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.decorators import method_decorator

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        
        if request.user.is_authenticated:
            completed_order_items = OrderItem.objects.filter(order__user=request.user, order__status='Completed')
            context['completed_order_items'] = completed_order_items
            context['has_completed_orders'] = completed_order_items.exists()
        
        
        context['books'] = Book.objects.all()  
        return render(request, 'dashboard.html', context)

class EbookReadView(View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return render(request, 'error.html', {'message': 'ไม่มีหนังสือในระบบ'})
        
        if not OrderItem.objects.filter(order__user=request.user, book=book).exists():
            return render(request, 'error.html', {'message': 'คุณไม่ได้ซื้อหนังสือเล่มนี้'})

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
    
    

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        # ดึง ID ของหนังสือในตะกร้าจาก session
        cart_ids = request.session.get('cart', [])
        
        # ดึงข้อมูลหนังสือที่อยู่ในตะกร้า
        books_in_cart = Book.objects.filter(id__in=cart_ids)

        context = {
            'books_in_cart': books_in_cart,
            'cart_count': len(cart_ids),
        }
        return render(request, 'cart.html', context)
    
class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        # ดึง ID ของหนังสือที่ต้องการลบออกจากตะกร้า
        cart = request.session.get('cart', [])
        
        # ถ้ามี ID ของหนังสือในตะกร้า ก็ลบออก
        if book_id in cart:
            cart.remove(book_id)
            request.session['cart'] = cart

        return redirect('cart')  # เปลี่ยนเส้นทางไปที่หน้า Cart

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        cart = request.session.get('cart', [])
    
        if book.id not in cart:
            cart.append(book.id)
            request.session['cart'] = cart

        return redirect('store')  # Redirect to your main page or wherever

@method_decorator(staff_member_required, name='dispatch')
class AdminAddBookView(View):
    def get(self, request):
        book_form = BookForm()
        context = {
            'book_form': book_form,
        }
        return render(request, 'admin_add_book.html', context)

    def post(self, request):
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save()
            messages.success(request, 'เพิ่มหนังสือใหม่เรียบร้อยแล้ว')
            return redirect('store')
        else:
            print(book_form.errors)  # เพิ่มบรรทัดนี้เพื่อแสดงข้อผิดพลาดในคอนโซล
            messages.error(request, 'พบข้อผิดพลาดในการเพิ่มหนังสือ')
            context = {
                'book_form': book_form,
            }
            return render(request, 'admin_add_book.html', context)


@method_decorator(staff_member_required, name='dispatch')
class AdminAddSerieView(View):
    def get(self, request):
        series_form = SerieForm()
        context = {
            'series_form': series_form,
        }
        return render(request, 'admin_add_serie.html', context)

    def post(self, request):
        series_form = SerieForm(request.POST)
        if series_form.is_valid():
            series_form.save()
            messages.success(request, 'เพิ่มซีรีส์ใหม่เรียบร้อยแล้ว')
            return redirect('admin_add_book')  # เปลี่ยนเป็น URL ที่เหมาะสม
        else:
            messages.error(request, 'พบข้อผิดพลาดในการเพิ่มซีรีส์')
            context = {
                'series_form': series_form,
            }
            return render(request, 'admin_add_serie.html', context)
        

@method_decorator(staff_member_required, name='dispatch')
class AdminAddAuthorView(View):
    def get(self, request):
        author_form = AuthorForm()
        context = {
            'author_form': author_form,
        }
        return render(request, 'admin_add_author.html', context)

    def post(self, request):
        author_form = AuthorForm(request.POST)
        if author_form.is_valid():
            author_form.save()
            messages.success(request, 'เพิ่มผู้เขียนใหม่เรียบร้อยแล้ว')
            return redirect('admin_add_serie')  # เปลี่ยนเป็น URL ที่เหมาะสม
        else:
            messages.error(request, 'พบข้อผิดพลาดในการเพิ่มผู้เขียน')
            context = {
                'author_form': author_form,
            }
            return render(request, 'admin_add_author.html', context)

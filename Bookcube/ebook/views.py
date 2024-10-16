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
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        cart_ids = request.session.get('cart', [])
        
        books_in_cart = Book.objects.filter(id__in=cart_ids)

        context = {
            'books_in_cart': books_in_cart,
        }
        return render(request, 'cart.html', context)
    
class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        cart = request.session.get('cart', [])
        
        if book_id in cart:
            cart.remove(book_id)
            request.session['cart'] = cart

        return redirect('cart')

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
class FavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        # ดึงรายการโปรดของผู้ใช้
        favorite_series = UserFavoriteSeries.objects.filter(user=request.user).select_related('series')

        context = {
            'favorite_series': favorite_series,
        }

        return render(request, 'favorites.html', context)

class AddToFavoritesView(LoginRequiredMixin, View):
    def post(self, request, series_id):
        series = get_object_or_404(BookSeries, id=series_id)

        # ตรวจสอบว่าซีรีส์อยู่ในรายการโปรดแล้วหรือไม่
        if not UserFavoriteSeries.objects.filter(user=request.user, series=series).exists():
            UserFavoriteSeries.objects.create(user=request.user, series=series)

        return redirect('search')  # เปลี่ยนเส้นทางไปที่หน้า Favorites


class RemoveFromFavoritesView(LoginRequiredMixin, View):
    def post(self, request, series_id):
        favorite = get_object_or_404(UserFavoriteSeries, user=request.user, series_id=series_id)
        favorite.delete()

        return redirect('favorites')
    
def notify_user_of_new_book(series, user):
    message = f"มีหนังสือใหม่ในซีรีย์ '{series.title}': {series.books.last.title}"
    Notification.objects.create(user=user, message=message)

@receiver(post_save, sender=Book)
def notify_users_of_new_book(sender, instance, created, **kwargs):
    if created:
        series = instance.series
        followers = UserFavoriteSeries.objects.filter(series=series).values_list('user', flat=True)
        for user_id in followers:
            user = User.objects.get(id=user_id)
            notify_user_of_new_book(series, user)

class NotificationView(LoginRequiredMixin, View):
    def get(self, request):
        notifications = request.user.notifications.all().order_by('-created_at')
        context = {
            'notifications': notifications,
        }
        return render(request, 'notifications.html', context)

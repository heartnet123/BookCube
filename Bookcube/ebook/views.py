from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
from django.db import models
from django.shortcuts import render, get_object_or_404
from .models import Book
from django.views import View

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        # รวบรวมข้อมูลสำหรับแดชบอร์ด
        context['total_books'] = Book.objects.count()
        context['total_sales'] = Order.objects.filter(status='Completed').count()
        
        # หนังสือขายดี (ตัวอย่าง: 3 อันดับแรก)
        context['best_selling_books'] = Book.objects.annotate(order_count=models.Count('orderitem')).order_by('-order_count')[:3]
        
        # หมวดหมู่ยอดนิยม (ตัวอย่าง: 3 อันดับแรก)  
        context['popular_categories'] = Category.objects.annotate(book_count=models.Count('book')).order_by('-book_count')[:3]
        
        # ข้อมูลสำหรับกราฟยอดขายรายเดือน (ตัวอย่าง)
        context['monthly_sales'] = [
            {'เดือน': 'มกราคม', 'ยอดขาย': 1000},
            {'เดือน': 'กุมภาพันธ์', 'ยอดขาย': 1200},
            {'เดือน': 'มีนาคม', 'ยอดขาย': 1500},
            # เพิ่มข้อมูลเดือนอื่นๆ ตามต้องการ
        ]
        context['books'] = Book.objects.all()  
        return render(request, 'dashboard.html', context)

class EbookReadView(View):
    def get(self, request, book_id, *args, **kwargs):
        book = get_object_or_404(Book, id=book_id)
        return render(request, 'ebook.html', {'book': book})
from django import forms
from django.forms import DateInput 
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'series', 'volume_number', 'published_date',
                  'cover_image', 'price', 'categories', 'ebook_file']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'series': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'volume_number': forms.NumberInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'published_date': forms.DateInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500', 'type': 'date'}),
            'cover_image': forms.FileInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'categories': forms.SelectMultiple(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'ebook_file': forms.FileInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        volume_number = cleaned_data.get('volume_number')

        if volume_number is not None and volume_number < 1:
            raise forms.ValidationError("Volume number must be at least 1.")

        return cleaned_data


class SerieForm(forms.ModelForm):
    class Meta:
        model = BookSeries
        fields = ['title', 'author']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'author': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'เขียนรีวิวที่นี่...', 'rows': 4, 'class': 'form-textarea'}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
        }
        labels = {
            'content': 'เนื้อหารีวิว',
            'rating': 'คะแนน',
        }
        help_texts = {
            'content': 'กรุณาให้รายละเอียดเกี่ยวกับหนังสือเล่มนี้',
            'rating': 'เลือกคะแนนจาก 1 ถึง 5'
        }
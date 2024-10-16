from django import forms
from django.forms import DateInput 
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'series', 'volume_number', 'published_date',
                  'cover_image', 'price', 'categories', 'ebook_file']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].queryset = Category.objects.all()
        self.fields['series'].queryset = BookSeries.objects.all()
        self.fields['published_date'].widget = DateInput(attrs={'type': 'date'})
    


class SerieForm(forms.ModelForm):
    class Meta:
        model = BookSeries
        fields = ['title', 'author']
    
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']  # กำหนดฟิลด์ที่ต้องการให้แสดงในฟอร์ม
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
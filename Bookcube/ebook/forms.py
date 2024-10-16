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

class BookFormEdit(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'series', 'volume_number', 'published_date',
                  'cover_image', 'price', 'categories', 'ebook_file']

    def __init__(self, *args, **kwargs):
        super(BookFormEdit, self).__init__(*args, **kwargs)
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].queryset = Category.objects.all()
        self.fields['series'].queryset = BookSeries.objects.all()
        self.fields['published_date'].widget = DateInput(attrs={'type': 'date'})
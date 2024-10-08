from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BookSeries(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='series')

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    series = models.ForeignKey(BookSeries, on_delete=models.CASCADE, related_name='books')
    volume_number = models.IntegerField()
    published_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categories = models.ManyToManyField(Category, through='BookCategory')
    ebook_file = models.FileField(upload_to='ebooks/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} (เล่ม {self.volume_number})"


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'category')

    def __str__(self):
        return f"{self.book.title} อยู่ในหมวด {self.category.name}"

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    review_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"รีวิวโดย {self.user.username} สำหรับ {self.book.title}"

class UserFavoriteSeries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_series')
    series = models.ForeignKey(BookSeries, on_delete=models.CASCADE, related_name='favorited_by_users')

    class Meta:
        unique_together = ('user', 'series')

    def __str__(self):
        return f"{self.user.username} ชื่นชอบ {self.series.title}"

class UserFavoriteAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_authors')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='favorited_by_users')

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f"{self.user.username} ชื่นชอบ {self.author.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"การแจ้งเตือนสำหรับ {self.user.username}: {self.message}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ตะกร้าของ {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} ในตะกร้าของ {self.cart.user.username}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"คำสั่งซื้อ {self.id} โดย {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} ในคำสั่งซื้อ {self.order.id}"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"การชำระเงิน {self.id} สำหรับคำสั่งซื้อ {self.order.id}"

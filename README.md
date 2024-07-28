

### Overview

In a Django REST API, it's useful to separate concerns to keep the codebase clean and maintainable. Two key patterns to achieve this are:

1. **Selectors**: Responsible for fetching data from the database.
2. **Services**: Responsible for handling business logic and operations that affect data.

By using selectors and services, we ensure that the logic for retrieving data is separate from the logic for manipulating data. This makes the code easier to understand, test, and maintain.



###Structure

Here's an updated structure where serializers leverage services for creating and updating data:

```
myproject/
│
├── myapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── selectors.py
│   ├── services.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_selectors.py
│   │   ├── test_services.py
│   │   └── test_views.py
│   └── migrations/
│       └── __init__.py
└── manage.py
```

### Models

```python
# myapp/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()

    def __str__(self):
        return self.title
```

### Selectors

```python
# myapp/selectors.py
from .models import Book

def get_all_books():
    return Book.objects.all()

def get_book_by_isbn(isbn):
    try:
        return Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return None
```

### Services

```python
# myapp/services.py
from .models import Book
from .selectors import get_book_by_isbn

def create_book(title, author, published_date, isbn, pages):
    book = Book(
        title=title,
        author=author,
        published_date=published_date,
        isbn=isbn,
        pages=pages
    )
    book.save()
    return book

def update_book(isbn, **kwargs):
    book = get_book_by_isbn(isbn)
    if book:
        for key, value in kwargs.items():
            setattr(book, key, value)
        book.save()
        return book
    return None

def delete_book(isbn):
    book = get_book_by_isbn(isbn)
    if book:
        book.delete()
        return True
    return False
```

### Serializers

In the serializers, we will use the services for creating and updating data.

```python
# myapp/serializers.py
from rest_framework import serializers
from .models import Book
from .services import create_book, update_book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def create(self, validated_data):
        return create_book(**validated_data)

    def update(self, instance, validated_data):
        return update_book(instance.isbn, **validated_data)
```

### Views

The views can remain the same, as they will use the serializers to handle data transformation and service calls.

```python
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .selectors import get_all_books, get_book_by_isbn
from .serializers import BookSerializer

class BookListView(APIView):
    def get(self, request):
        books = get_all_books()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    def get(self, request, isbn):
        book = get_book_by_isbn(isbn)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, isbn):
        book = get_book_by_isbn(isbn)
        if book:
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, isbn):
        if delete_book(isbn):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
```

### URLs

```python
# myapp/urls.py
from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<str:isbn>/', BookDetailView.as_view(), name='book-detail'),
]
```

### Testing

Ensure your tests cover the integration of services within serializers:

```python
# myapp/tests/test_selectors.py
from django.test import TestCase
from myapp.models import Book
from myapp.selectors import get_all_books, get_book_by_isbn

class BookSelectorTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date="2023-01-01",
            isbn="1234567890123",
            pages=100
        )

    def test_get_all_books(self):
        books = get_all_books()
        self.assertIn(self.book, books)

    def test_get_book_by_isbn(self):
        book = get_book_by_isbn("1234567890123")
        self.assertEqual(book, self.book)
```

```python
# myapp/tests/test_services.py
from django.test import TestCase
from myapp.models import Book
from myapp.services import create_book, update_book, delete_book

class BookServiceTest(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890123",
            "pages": 100
        }
        self.book = create_book(**self.book_data)

    def test_create_book(self):
        book = create_book(**self.book_data)
        self.assertIsNotNone(book.id)

    def test_update_book(self):
        updated_book = update_book(self.book.isbn, title="Updated Test Book")
        self.assertEqual(updated_book.title, "Updated Test Book")

    def test_delete_book(self):
        result = delete_book(self.book.isbn)
        self.assertTrue(result)
        self.assertIsNone(Book.objects.filter(isbn=self.book.isbn).first())
```

This structure ensures a clear separation of concerns while integrating services within serializers, keeping your codebase clean and maintainable.

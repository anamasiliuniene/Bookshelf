from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance


# Create your views here.
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'bookshelf/index.html', context=context)


def authors(request):
    context = {
        'authors': Author.objects.all(),
    }
    return render(request, 'bookshelf/authors.html', context=context)

def author(request, author_id):
    context = {
        'author': Author.objects.get(pk=author_id),
    }
    return render(request, 'bookshelf/author.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'bookshelf/books.html'
    context_object_name = 'books'
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'bookshelf/book.html'
    context_object_name = 'book'

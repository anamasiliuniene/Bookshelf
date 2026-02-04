from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance
from django.core.paginator import Paginator
from django.db.models import Q

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
    authors = Author.objects.all()
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
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

def search(request):
    query = request.GET.get('query')
    context = {
        "query": query,
        "books": Book.objects.filter(Q(title__icontains=query) |
                                     Q(author__first_name__icontains=query) |
                                     Q(author__last_name__icontains=query) |
                                     Q(summary__icontains=query)),

        "authors": Author.objects.filter (Q(first_name__icontains=query) |
                                     Q(last_name__icontains=query))
    }
    return render(request, 'bookshelf/search.html', context=context)
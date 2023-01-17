from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
def index(request):
    # count užklausos(queries)
    num_books = Book.objects.all().count() # suskaičiuojam kiek biblioteka turi knygų
    num_instances = BookInstance.objects.all().count()


    # suskaičiuosime laisvas knygas(statusas g)
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # suskaičiuojam autorius
    num_authors = Author.objects.all().count()

    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors
               }
    return render(request, 'index.html', context=context) # html failo atvaixdavimas

def authors(request):

    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context=context)

def author(request):

    author = Author.objects.all()


# Create your views here.

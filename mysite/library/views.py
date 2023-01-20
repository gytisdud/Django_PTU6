from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
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

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors,
               'num_visits': num_visits
               }
    return render(request, 'index.html', context=context) # html failo atvaixdavimas


def authors(request):
    # authors = Author.objects.all()
    paginator = Paginator(Author.objects.all(), 1)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)

    context = {
        'authors': paged_authors
    }
    return render(request, 'authors.html', context=context)

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})

def search(request):
    query = request.GET.get("query")
    search_results = Book.objects.filter(
                                Q(title__icontains=query) |
                                Q(summary__icontains=query)
    )
    return render(request, "search.html", {"books": search_results, "query": query})

class BookListView(generic.ListView):
    model = Book # pagal modelio pav. sukuriamas book_list kintamasis(visi obj is klases) perdudamas i sablona
    paginate_by = 1
    template_name = 'book_list.html' # context_object_name = 'my_book_list' galime pakeisti automatini konteksto kontamaji(book_list)


class BookDetailView(generic.DetailView):
    model = Book # sukurs book kintamaji sablonui
    template_name = 'book_detail_style.html'


# Create your views here.

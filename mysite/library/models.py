from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Įveskite knygos žanrą')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
class Book(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books')
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Išrinkite žanrą/us šiai knygai')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()])
    display_genre.short_description = 'Genre'
    def __str__(self):
        return f"{self.title} {self.isbn}"

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus knygos kopijos ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )


    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Status'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} {self.book.title}'

class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    description = models.TextField('Aprašymas', max_length=2000, default='bio')
    def display_books(self):
        return ', '.join([book.title for book in self.books.all()])
    display_books.short_description = 'Knygos'
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}  {self.first_name}'
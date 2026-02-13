import uuid
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    description = HTMLField(verbose_name="Description", max_length=3000, default="")

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    display_books.short_description = "Books"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(to="Author",
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name="books")
    summary = models.TextField()
    isbn = models.CharField(max_length=13)
    genre = models.ManyToManyField(to="Genre")
    cover = models.ImageField(upload_to="covers", null=True, blank=True)

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    display_genre.short_description = "Genre"

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="photos", null=True, blank=True)


class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4)
    book = models.ForeignKey(to="Book",
                             verbose_name="Book",
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name="instances")

    due_back = models.DateField(null=True, blank=True)
    reader = models.ForeignKey(to="bookshelf.CustomUser",
                               verbose_name="Reader",
                               on_delete=models.SET_NULL,
                               null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Administered'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(verbose_name="Status", max_length=1, choices=LOAN_STATUS, blank=True, default="d")

    @property
    def is_overdue(self):
        return self.due_back and self.due_back < now().date()

    def __str__(self):
        return f"{self.book} ({self.uuid})"


class BookReview(models.Model):
    book = models.ForeignKey(to="Book", verbose_name="Book", on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="reviews")
    reviewer = models.ForeignKey(to="bookshelf.CustomUser", verbose_name="Reviewer", on_delete=models.SET_NULL,
                                 null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    content = models.TextField(verbose_name="Content", max_length=2000)

    class Meta:
        verbose_name = "Book Review"
        verbose_name_plural = "Book Reviews"
        ordering = ["-date_created"]





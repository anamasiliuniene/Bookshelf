from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "display_genre"]
    inlines = [BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ["book", "status", "due_back", "uuid"]
    list_filter = ["book", "status", "due_back"]

    fieldsets = (
    ('General', {
        'fields': ('book', 'uuid'),
    }),
    ('Availability', {
        'fields': ('status', 'due_back'),
    }),
)

# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("short_name", "display_books")

    def short_name(self, obj):
        if obj.first_name:
            return f"{obj.last_name}, {obj.first_name[0]}."
        return obj.last_name

    short_name.short_description = "Author"
    short_name.admin_order_field = "last_name"

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    can_delete = False
    readonly_fields = ['uuid']
    fields = ['status', 'due_back', 'uuid', 'reader']

class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "display_genre"]
    inlines = [BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ["book", "status", "due_back", 'reader', "uuid"]
    list_filter = ["book", "status", "due_back"]
    search_fields = ["book__title", "book__author__last_name", "uuid"]
    list_editable = ["status", 'reader', "due_back"]

    fieldsets = (
    ('General', {
        'fields': ('book', 'uuid'),
    }),
    ('Availability', {
        'fields': ('status', 'due_back', 'reader'),
    }),
)

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

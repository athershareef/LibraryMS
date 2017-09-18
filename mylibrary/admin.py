from django.contrib import admin
from .models import BookLoans, Borrower, Authors, Book, BookAuthors, Fines

# Register your models here.

admin.site.register(Authors)
admin.site.register(BookAuthors)


class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'ssn', 'bname', 'address', 'phone')
    list_per_page = 25


class BookLoansAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'date_out', 'due_date', 'date_in', 'card_id', 'isbn_id')
    list_per_page = 25
    raw_id_fields = ("isbn", "card_id")
    search_fields = ("isbn",)


class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title')
    list_per_page = 25


class FinesAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'fine_amt', 'paid')
    list_per_page = 25
    raw_id_fields = ("loan_id",)
    search_fields = ("loan_id",)


admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(BookLoans, BookLoansAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Fines, FinesAdmin)

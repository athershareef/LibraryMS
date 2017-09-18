import sys, os, django, csv
from tqdm import tqdm
from mylibrary.models import Authors, Book, BookAuthors, Borrower

sys.path.append("C:/Users/ather/PycharmProjects/LMS/LMS")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LMS.settings")
django.setup()


def loadAuthor():
    datareader = csv.reader(open('author.csv'), delimiter=',', quotechar='"')
    for row in tqdm(datareader):
        if row[0] != 'Author':
            author = Authors()
            author.name = row[0]
            author.save()


def loadBooks():
    datareader = csv.reader(open('book.csv'), delimiter=',', quotechar='"')
    for row in tqdm(datareader):
        if row[0] != 'ISBN10':
            book = Book()
            book.isbn = row[0]
            book.title = row[1]
            book.save()


def loadBookAuthors():
    datareader = csv.reader(open('book_authors.csv'), delimiter=',', quotechar='"')
    for row in tqdm(datareader):
        if row[0] != 'author_id':
            ba = BookAuthors()
            author = Authors.objects.get(author_id=row[0])
            book = Book.objects.get(isbn=row[1])
            ba.author_id = author
            ba.isbn = book
            ba.save()


def loadBorrowers():
    datareader = csv.reader(open('borrowers.csv'), delimiter=';', quotechar='"')
    for row in tqdm(datareader):
        if row[0] != 'card_id':
            borrower = Borrower()
            borrower.card_id = row[0]
            borrower.ssn = row[1]
            borrower.bname = row[2]
            borrower.address = row[3]
            borrower.phone = row[4]
            borrower.save()


def loadBookAuthors():
    datareader = csv.reader(open('book_authors.csv'), delimiter=',', quotechar='"')
    for row in tqdm(datareader):
        if row[0] != 'author_id':
            ba = BookAuthors()
            author = Authors.objects.get(author_id=row[0])
            book = Book.objects.get(isbn=row[1])
            ba.author_id = author
            ba.isbn = book
            ba.save()


loadBorrowers()

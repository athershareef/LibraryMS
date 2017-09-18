from django.db import models
from datetime import date
from datetime import timedelta


# Create your models here.

class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=200)

    def __str__(self):
        return "ISBN: " + self.isbn + ", Title: " + self.title


class Authors(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "Author ID: " + str(self.author_id) + ", Title: " + str(self.name)


class BookAuthors(models.Model):
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return "Author ID: " + str(self.author_id) + ", ISBN: " + str(self.isbn)


class Borrower(models.Model):
    card_id = models.AutoField(primary_key=True)
    ssn = models.CharField(max_length=9, unique=True)
    bname = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self):
        string = "Card ID: " + str(
            self.card_id) + ",Borrower's Name: " + self.bname
        return string


class BookLoans(models.Model):
    loan_id = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE,
                             error_messages={'unique': "This email has already been registered."})
    card_id = models.ForeignKey(Borrower, on_delete=models.CASCADE,
                                error_messages={'unique': "This email has already been registered."})
    date_out = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=date.today() + timedelta(days=14))
    date_in = models.DateField(blank=True, null=True)

    def __str__(self):
        string = "Loan ID: " + str(self.loan_id) + ", ISBN: " + str(self.isbn) + ", Card ID: " + str(
            self.card_id) + ", Date Out: " + str(self.date_out) + ", Due Date: " + str(
            self.due_date) + ", Date In: " + str(self.date_in)
        return string

    def save(self, *args, **kwargs):
        count = BookLoans.objects.filter(card_id=self.card_id, date_in__isnull=True).count()
        duplicate = BookLoans.objects.filter(isbn=self.isbn, date_in__isnull=True).count()
        print(count, duplicate)
        if duplicate > 0:
            if self.date_in is None:
                raise UserWarning("Book is already Checked out to the other Borrower")
            else:
                super(BookLoans, self).save(*args, **kwargs)
        elif count > 2:
            if self.date_in is None:
                raise UserWarning("Please Make sure that a Single User can have no more than 3 books checked out")
        else:
            super(BookLoans, self).save(*args, **kwargs)


class Fines(models.Model):
    loan_id = models.OneToOneField(BookLoans, primary_key=True)
    fine_amt = models.DecimalField(max_digits=5, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "Loan ID: " + str(self.loan_id) + ", Fine Amount: " + str(self.fine_amt) + ",Paid? : " + str(self.paid)

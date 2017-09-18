from django.shortcuts import render
from django.db import connection

from .models import BookLoans


def fines(request):
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO mylibrary_fines (loan_id_id, fine_amt,paid) SELECT 
    loan_id, 0, FALSE
FROM
    mylibrary_bookloans
WHERE
    loan_id NOT IN (SELECT 
            loan_id_id
        FROM
            mylibrary_fines)
        AND DATEDIFF(date_in, due_date) > 0
        AND date_in IS NOT NULL 
UNION SELECT 
    loan_id, 0, FALSE
FROM
    mylibrary_bookloans
WHERE
    loan_id NOT IN (SELECT 
            loan_id_id
        FROM
            mylibrary_fines)
        AND DATEDIFF(DATE(NOW()), due_date) > 0
        AND date_in IS NULL;
        REPLACE INTO mylibrary_fines (loan_id_id, fine_amt,paid) SELECT 
                loan_id, DATEDIFF(date_in, due_date) * 0.25, paid
            FROM
                mylibrary_bookloans,
                mylibrary_fines
            WHERE
                loan_id_id=loan_id AND
                DATEDIFF(date_in, due_date) > 0
                    AND date_in IS NOT NULL 
            UNION SELECT 
                loan_id, DATEDIFF(DATE(NOW()), due_date) * 0.25, paid
            FROM
               mylibrary_bookloans,
                mylibrary_fines
            WHERE
                loan_id_id=loan_id AND
                DATEDIFF(DATE(NOW()), due_date) > 0
                    AND date_in IS NULL''')
    return render(request, 'basic/fines.html', {'val': 1})


# def bsearch(request):
#     if request.method == "POST":
#         val = request.POST['search_key']
#         # ids = Authors.objects.filter(name__icontains=val).values_list('id', flat=True)
#         books_qs = Book.objects.filter(isbn__icontains=val).va | Book.objects.filter(
#             isbn__icontains=val) | Book.objects.filter()
#         if books_qs.count() == 0:
#             print("No Values found")
#         # for each in books_qs:
#         #     print(each)
#         dict['last_phrase'] = request.POST['search_key']
#         dict['book_qs'] = books_qs
#         books_table = BookTable(books_qs)
#         dict['books_table'] = books_table
#     return render(request, 'basic/bsearch.html', dict)
#

def payfine(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT 
                        card_id_id,
                        group_concat(loan_id),
                        SUM(fine_amt),
                        paid,
                        (SELECT 
                                CASE
                                        WHEN (date_in IS NULL) THEN 'Cannot Pay without all books checked in'
                                        ELSE 'pay'
                                    END
                            ) AS PAY
                    FROM
                        mylibrary_fines AS f,
                        mylibrary_bookloans AS bl
                    WHERE
                        f.loan_id_id = bl.loan_id
                            AND paid = 'false'
                    GROUP BY card_id_id
                            ''')
    data = cursor.fetchall()
    dict = {}
    dict['data'] = data
    return render(request, 'basic/payfine.html', dict)


def bsearch(request):
    # book_all = Book.objects.all()
    dict = {}
    if request.method == "POST":
        key = request.POST['search_key']
        cursor = connection.cursor()
        cursor.execute('''SELECT 
                b.bname, b.card_id, bl.isbn_id
            FROM
                mylibrary_borrower AS b,
                mylibrary_bookloans AS bl
            WHERE
                b.card_id = bl.card_id_id 
                    AND date_in IS NULL
                    AND (b.bname LIKE '%''' + key + '''%'
                    OR bl.isbn_id LIKE '%''' + key + '''%'
                    OR b.card_id LIKE '%''' + key + '''%')''')
        data = cursor.fetchall()
        loandict = {}
        for row in data:
            loandict[row[2]] = list(
                BookLoans.objects.filter(isbn=row[2], card_id=row[1]).values_list('loan_id', flat=True))
        dict['last_phrase'] = request.POST['search_key']
        dict['data'] = data
        dict['loandict'] = loandict
    return render(request, 'basic/bsearch.html', dict)


def customsearch(request):
    dict = {}
    if request.method == "POST":
        key = request.POST['search_key']
        cursor = connection.cursor()
        cursor.execute('''SELECT 
                b.isbn,
                b.title,
                GROUP_CONCAT(a.name),
                (SELECT 
                        CASE
                                WHEN
                                    (SELECT 
                                            COUNT(*)
                                        FROM
                                            mylibrary_bookloans AS bl
                                        WHERE
                                           bl.isbn_id = b.isbn
                                    AND (bl.date_in IS NULL
                                    AND bl.due_date > DATE(NOW()))) > 0
                                THEN
                                    'I'
                                ELSE 'O'
                            END
                    ) AS status
            FROM
                                    mylibrary_book AS b,
                                    mylibrary_authors AS a,
                                    mylibrary_bookauthors AS ba
                                WHERE
                                    (b.isbn = ba.isbn_id AND
                                    ba.author_id_id=a.author_id) AND
                                    (b.title LIKE '%''' + key + '''%' OR b.isbn LIKE '%''' + key + '''%' OR a.name LIKE '%''' + key + '''%')
                                GROUP BY b.isbn,b.title''')
        data = cursor.fetchall()
        loandict = {}
        for row in data:
            loandict[row[0]] = list(BookLoans.objects.filter(isbn=row[0]).values_list('loan_id', flat=True))
        dict['last_phrase'] = request.POST['search_key']
        dict['data'] = data
        dict['loandict'] = loandict
    return render(request, 'basic/search.html', dict)

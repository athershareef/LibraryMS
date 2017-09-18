# LibraryMS
Creation of a Web application that interfaces with a back-end SQL database implementing a Library Management System


Quick Start Guide of Alan Turing Library
Search:
Performs a case insensitive search based on any of ISBN, title, and Author. The Check In/Check Out column helps in check in and check outs of the books. If the book is available, then only check out link is generated. On the other hand, when the book is returned by the loaners, click to check in link is available so that the user can take the book back, which makes is available to be taken by others. While check out, make sure to leave the date_in as blank and when the borrower returns the book for checkin, please make sure to have a date_in as today’s value by clicking on today in checkin admin tab.
 
Navigation Bar:
Helps Librarian for quick navigation.
 
Add Borrowers:
	Allows the user to add borrowers to be Library database. Note that all fields in add borrowers are mandatory. 
Check In by Borrower’s details:
	This page helps the user to check in books by borrowers details (name or card_id) which helps to check all the books for a given borrower/loaner.
 
Run Fines:
	It helps to identify the amount which needs to be paid be every borrower. In production, it happens automatically with a Cron Job.
Pay Fines:
	This page helps the user to retrieve the sum of amounts per card_id i.e. for each borrower, all the pending amount is shown in the UI. If all the books are checked in, Pay Fine now link with be available, else borrowers must checkin their books in order to clear the dues.
 

Note:
All the Update/Delete/Insert operations are done via a secured login. i.e. only admin who is having the password will be able to perform the operations.
Tip: When in admin mode, click on View Site to go back to the home page.
ID having all access:
User ID: athershareefvce@gmail.com
Password: ather1234

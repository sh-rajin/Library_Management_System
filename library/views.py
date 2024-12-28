from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView,ListView, View
from .models import Report
from django.contrib.auth.decorators import login_required
from categories.models import Category
from books.models import Book
from .import forms
from django.utils.timezone import datetime
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
# Create your views here.

def send_transaction_mail(account,book,subject,template):
    
    user = account.user
    
    mail_message = render_to_string(template, {
        'user': user,
        'book_title': book.title,
        'time': timezone.now(),
    })
        
    send_mail = EmailMultiAlternatives(subject, '' , to=[user.email])
    send_mail.attach_alternative(mail_message, 'text/html')
    send_mail.send()


class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            return Book.objects.filter(category=category)
        return Book.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context
    
    
    
class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Book.objects.get(id=book_id)
        review_form = forms.ReviewForm()  # Initialize an empty form
        reviews = book.reviews.all()  # Fetch all reviews for the book
        return render(request, 'library/details.html', {
            'book': book,
            'reviews': reviews,
            'form': review_form,  # Pass the form to the template
        })

    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        try:
            report_book = Report.objects.get(book_id=book_id, user=self.request.user.account)
            review_form = forms.ReviewForm(data=request.POST) 
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.book = report_book.book 
                new_review.user = self.request.user.account 
                new_review.save()

                messages.success(request, "Your review has been submitted.")
                return redirect('book_detail', id=book_id)

            # Render the page with form errors if the form is invalid
            reviews = report_book.book.reviews.all()
            return render(request, 'books/details.html', {
                'book': report_book.book,
                'reviews': reviews,
                'form': review_form,
            })

        except Report.DoesNotExist:
            # Handle the case where the user has not borrowed the book
            messages.error(request, "You can only review books you have borrowed.")
            return redirect('book_detail', id=book_id)

  
    
    
class BorrowBookView(View):
    
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Book.objects.get(id=book_id)
        user_account = request.user.account
        
        if user_account.balance >= book.price:
            # Check if the user has already borrowed this book and not returned it
            borrowed_book = Report.objects.filter(book=book, user=request.user.account, is_returned=False).first()
            
            if borrowed_book:
                messages.error(request, 'Book already borrowed!')
            else:
                # Deduct balance for borrowing
                user_account.balance -= book.price
                user_account.save()

                # Create a new borrowing record
                Report.objects.create(
                    user=user_account,
                    book=book,
                )
                messages.success(request, f"Successfully borrowed '{book.title}'!")
                send_transaction_mail(user_account,book, 'Borrowing', 'library/borrow_book_mail.html')
                return redirect('profile')
        else:
            messages.error(request, 'Insufficient balance!')
            return redirect('home')
    

    
    
class ReturnBookView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        borrowed_book = get_object_or_404(Report, id=book_id, user=request.user.account, is_returned=False)

        borrowed_book.is_returned = True
        borrowed_book.save()

        book = borrowed_book.book
        user_account = borrowed_book.user
        user_account.balance += book.price
        user_account.save()

        messages.success(request, f"You have successfully returned '{book.title}'!")
        send_transaction_mail(user_account, book, 'Return Book', 'library/return_book_mail.html')
        
        return redirect('profile')
           
            
    
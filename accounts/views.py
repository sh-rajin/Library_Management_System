from django.shortcuts import render, redirect
from django.views.generic import FormView,ListView,View
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, DepositForm, UserAccountUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from library.models import Report
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
# Create your views here.

def send_transaction_mail(account,amount,subject,template):
    
    user = account.user
    
    mail_message = render_to_string(template, {
        'user': user,
        'amount': amount,
        'time': timezone.now(),
    })
        
    send_mail = EmailMultiAlternatives(subject, '' , to=[user.email])
    send_mail.attach_alternative(mail_message, 'text/html')
    send_mail.send()

class UserRagistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request,"Registration successfull!")
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    
    def get_success_url(self):
        messages.success(self.request,"Login successfull!")
        return reverse_lazy('home')
    
       
class UserLogoutView(LogoutView):
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(self.request,"Logout successfull!")
        return redirect('user_login')
    
    
class DepositMoneyView(FormView):
    form_class = DepositForm
    template_name = 'accounts/deposit.html'

    def form_valid(self, form):
        deposit_amount = form.cleaned_data.get('amount')
        user_library_account = self.request.user.account
        user_library_account.balance += deposit_amount
        user_library_account.save()
        messages.success(self.request, f"{deposit_amount} Deposit successfull!")
        send_transaction_mail(user_library_account, deposit_amount, 'Deposit successful','accounts/deposit_mail.html')
        return redirect('home')
    

class ProfileView(View):
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        # print(request.user)
        user_library_account = self.request.user.account
        reports = Report.objects.filter(user=self.request.user.account)
        # for report in reports:
            # print(report.id)
            # print(report.book.title)
            # print(report.is_returned)
        return render(request, self.template_name, {'user_library_account': user_library_account, 'reports': reports})
    

    
    
class UserAccountUpdateView(View):
    template_name = 'accounts/profile_update.html'

    def get(self, request):
        # print(request.user)
        form = UserAccountUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserAccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Profile updated successfully!")
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
    



class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        mail_message = render_to_string('accounts/pass_change_mail.html', {
            'user': self.request.user,
            'time': timezone.now(),
        })
            
        email = EmailMultiAlternatives(
            subject='Password Change',
            body='',
            to=[self.request.user.email],
        )
        email.attach_alternative(mail_message, 'text/html')
        email.send()
        
        return response
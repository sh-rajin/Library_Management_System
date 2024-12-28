from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
from . models import DepositModel, UserLibraryAccount, UserAddress

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'gender',
                  'street', 'city', 'postal_code', 'country', 'password1', 'password2']
        
    def save(self, commit = True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street = self.cleaned_data.get('street')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            
            UserAddress.objects.create(
                user=user,
                street=street,
                city=city,
                postal_code=postal_code,
                country=country,
            )
            UserLibraryAccount.objects.create(
                user=user,
                birth_date=birth_date,
                gender=gender,
                library_card_no = f"LIB-{str(user.id).zfill(6)}"
            )
            return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance  block w-full bg-gray-200'
                    ' text-gray-700 border-gray-200 rounded'
                    ' py-3 px-4 leading-tight'
                    ' focus:bg-white focus:border-gray-500'
                )
            })
 
 
 
class UserAccountUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance  block w-full bg-gray-200'
                    ' text-gray-700 border-gray-200 rounded'
                    ' py-3 px-4 leading-tight'
                    ' focus:bg-white focus:border-gray-500'
                )
            })
                
                
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
                # print(user_account)
                # print(user_address)
            except UserLibraryAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                # print(user_account.account_type)
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street'].initial = user_address.street
                # print(user_address.street)
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account = UserLibraryAccount.objects.get(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            user_address = UserAddress.objects.get(user=user) 

            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street = self.cleaned_data['street']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
    
 
            
            
class DepositForm(forms.ModelForm):
    class Meta:
        model = DepositModel
        fields = ('amount',)
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        min_deposit_amount = 100
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'Minimum Deposit amount is {min_deposit_amount}.')
        return amount
            
            
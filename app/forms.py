from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Librarian
from .models import IssuedBook
from .models import Book, Users


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [ 'Barcode','Title', 'Subtitle', 'Subject','Cl_No','author', 'Publisher','Publication_place', 'Publication_date','Language', 'dimensions',
                  'Page_count', 'isbn', 'category', 'Keyword',
                   'Price', 'Profile_pic', 'Description']
        widgets = {
            'Publication_date': forms.DateInput(attrs={'type': 'date'}),
            'Profile_pic': forms.ClearableFileInput(attrs={'multiple': False}),
            'Description': forms.Textarea(attrs={'rows': 4}),
        }

class IssuedBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['Barcode', 'national_id']

    Barcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'book-barcode'}),
        label='Book Barcode'
    )
    
    national_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'user-national-id'}),
        label='User National ID'
    )

    def clean_Barcode(self):
        barcode = self.cleaned_data.get('Barcode')
        if not Book.objects.filter(Barcode=barcode).exists():
            raise forms.ValidationError("This book does not exist.")
        if IssuedBook.objects.filter(Barcode=barcode, returned=False).exists():
            raise forms.ValidationError("This book has already been issued to another user.")
        return barcode

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if not Users.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("This user does not exist.")
        return national_id

class ReturnBookForm(forms.Form):
    Barcode = forms.CharField(max_length=100, label='Book Barcode')
    national_id = forms.CharField(max_length=100, label='National ID')
    
class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ['national_id', 'phone_number']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class EditProfileForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Current Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Validate current password
        if old_password and not self.instance.check_password(old_password):
            self.add_error('old_password', 'Current password is incorrect.')

        # Validate new passwords match
        if new_password1 and new_password1 != new_password2:
            self.add_error('new_password2', 'New passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get('new_password1')

        if new_password1:
            user.set_password(new_password1)
        
        if commit:
            user.save()
        
        return user



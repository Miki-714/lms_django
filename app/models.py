from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from datetime import date
from django import forms



class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=100)
    national_id_image = models.ImageField(upload_to='national_id_images/', null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} ({self.national_id})"


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('History', 'History'),
        # Add more categories as needed
    ]
    Barcode = models.CharField(max_length=200, unique=True)
    Title = models.CharField(max_length=200)
    Subtitle = models.CharField(max_length=200,null=True, default=None)
    Subject = models.CharField(max_length=200,null=True, default=None)
    Cl_No = models.CharField(max_length=200,null=True, default=None)
    author = models.CharField(max_length=200,null=True, default=None)
    Publisher = models.CharField(max_length=200,null=True, default=None)
    Publication_place = models.CharField(max_length=200,null=True, default=None)
    Publication_date = models.DateField(null=True, blank=True, default=None)
    Language = models.CharField(max_length=200,null=True, default=None)
    dimensions = models.CharField(max_length=50,null=True, default=None)  
    Page_count = models.IntegerField(null=True, default=None)
    isbn = models.PositiveIntegerField(null=True, default=None)
    category = models.CharField(max_length=50,null=True,choices=CATEGORY_CHOICES, default=None)
    Keyword = models.CharField(max_length=200,null=True, default=None)
    Price = models.FloatField(null=True, default=None)
    Profile_pic = models.ImageField(upload_to='book_images/', blank=True, null=True, default=None)
    Description = models.CharField(max_length=2000,null=True, default=None)

    def __str__(self):
        return f"{self.Title} - {self.dimensions} [{self.Barcode}]"

def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook(models.Model):
    Barcode = models.CharField(max_length=100, default='UNKNOWN')
    national_id = models.CharField(max_length=100, blank=True, null=True)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)
    returned = models.BooleanField(default=False)
    book = models.ForeignKey(Book,default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    
    
    @property
    def fine(self):
        if date.today() > self.expirydate and not self.returned:
            # Example fine calculation: $1 per day overdue
            delta = date.today() - self.expirydate
            return delta.days * 1
        return 0

    def __str__(self):
        return f"{self.Barcode} issued to {self.national_id}"

class ReturnBook(models.Model):
    Barcode = models.CharField(max_length=100)
    national_id = models.CharField(max_length=100)
    returndate = models.DateField(auto_now_add=True)
    
    book = models.ForeignKey(Book,default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Barcode} returned by {self.national_id} on {self.returndate}"
        
class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Add custom styles or classes here
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
from datetime import date
from django.core.mail import send_mail
from lms import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from . tokens import generate_token
from django.db.models import Q
from . models import *
from . forms import *
from django.http import HttpResponse
from .scanner.qr_scanner import scan_qr_code
from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LibrarianForm, UserForm
from .models import Librarian
from django.contrib.auth.decorators import user_passes_test
from .models import Book


from django.http import JsonResponse
from .models import IssuedBook, Users  # Import your models


from django.shortcuts import render, get_object_or_404
from .models import IssuedBook, Users, Book
from .forms import IssuedBookForm



def index(request):
    return render(request, 'app/index.html')

def core(request):
    return render(request, 'app/core.html')

def support(request):
    return render(request, 'app/support.html')

@login_required(login_url='/signin')
def profile(request):
    return render(request, 'app/profile.html')

# admin
def admin_login(request):

    if request.user.is_authenticated:
        return redirect('profile')

    else:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_superuser:
                    login(request, user)
                    return redirect('profile')

                else:
                    messages.error(
                        request, "This is an Student account. Please Sign-In here.")
                    return redirect('signinpage')

            else:
                messages.error(request, "Invalid Username & Password.")

        return render(request, "app/admin_login.html")


def signin(request):

    if request.user.is_authenticated:
        return redirect('profile')

    else:

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:

                if not user.is_superuser:
                    login(request, user)
                    return redirect('profile')

                else:
                    messages.error(
                        request, "This is an ADMIN account. Please Sign-In here.")
                    return redirect('admin_login')

            else:
                messages.error(
                    request, "Invalid Username & Password or Account not activated.")

        return render(request, 'app/signin.html')

# librarian
def librarian(request):

    if request.user.is_authenticated:
        return redirect('profile')

    else:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_staff:
                    login(request, user)
                    return redirect('profile')

                else:
                    messages.error(
                        request, "This is an Student account. Please Sign-In here.")
                    return redirect('signinpage')

            else:
                messages.error(request, "Invalid Username & Password.")

        return render(request, "app/admin_login.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            national_id = request.POST['national_id']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            national_id_image = request.FILES.get('national_id_image')

            # Validate form data
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists! Please try another username.")
                return redirect('signuppage')

            if len(username) > 20:
                messages.error(request, "Username must be under 20 characters.")
                return redirect('signuppage')

            if not username.islower():
                messages.error(request, "Username must be in lowercase.")
                return redirect('signuppage')

            if User.objects.filter(email=email).exists():
                messages.error(request, "E-Mail ID already registered.")
                return redirect('signinpage')

            if password != confirm_password:
                messages.error(request, "Passwords did not match.")
                return redirect('signuppage')

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            # Create Users model instance
            if not national_id_image:
                messages.error(request, "National ID image is required.")
                return redirect('signuppage')

            student = Users.objects.create(
                user=user,
                national_id=national_id,
                national_id_image=national_id_image
            )
            student.save()

            # Send activation email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            current_site = get_current_site(request)
            subject = "Welcome to LMS!"
            message = f"Hello {user.username}!\n\nWelcome to LMS. Your account has been created successfully. Please click the link below to activate your account.\n\nConfirmation Link: http://{current_site.domain}/activate/{uidb64}/{token}\n\nRegards\nTeam LMS"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            messages.success(request, "Activation email sent to your registered email address.")

        return render(request, "app/signup.html")

def activate(request, uidb64, token):

    if request.user.is_authenticated:
        return redirect('profile')

    else:

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Your account has been activated!")
            return redirect('signinpage')

        else:
            return render(request, 'activation_failed.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def forgetpass(request):

    if request.user.is_authenticated:
        return redirect('profile')

    else:
        return render(request, 'app/forgetpass.html')

from django.contrib import messages
from .forms import BookForm
@login_required(login_url='/admin_login')
def addbook(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book is added successfully.")
            return redirect('addbook')  # Redirect to the same page or another page after success
    else:
        form = BookForm()

    return render(request, "app/addbook.html", {'form': form})



def viewbook(request):
    search_query = request.GET.get('search_query', '')

    
    books = Book.objects.filter(
            Q(Title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query) |
            Q(Cl_No__icontains=search_query) |
            Q(Subject__icontains=search_query) |
            Q(Keyword__icontains=search_query) |
            Q(Barcode__icontains=search_query) |
            Q(category__icontains=search_query)
        )
   

    return render(request, "app/viewbook.html", {'books': books})

@login_required(login_url='/admin_login')
def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect('viewbook')


@login_required(login_url='/admin_login')
def view_student(request):
    # Get the search query from the request
    search_query = request.GET.get('search_student', '')
    
    # Filter the queryset based on the search query
    if search_query:
        students = Users.objects.filter(national_id__icontains=search_query)
    else:
        students = Users.objects.all()
    
    # Add a URL to the national_id_image field if it exists
    for student in students:
        if not student.national_id_image:
            student.national_id_image_url = ''  # Or use a placeholder image URL
        else:
            student.national_id_image_url = student.national_id_image.url

    return render(request, 'app/view_student.html', {'students': students})


@login_required(login_url='/admin_login')
def delete_student(request, myid):
    students = Users.objects.filter(id=myid)
    students.delete()
    return redirect('view_student')

from .forms import EditProfileForm
@login_required(login_url='/signin')


def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'app/editprofile.html', {'form': form})


@login_required(login_url='/admin_login')
def issuebook_view(request):
    if request.method == 'POST':
        form = IssuedBookForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['Barcode']
            national_id = form.cleaned_data['national_id']

            try:
                book = Book.objects.get(Barcode=barcode)
                user = Users.objects.get(national_id=national_id).user  # Assuming Users has a OneToOneField with User

                # Check if the book is already issued
                if IssuedBook.objects.filter(Barcode=barcode, returned=False).exists():
                    form.add_error('Barcode', "This book has already been issued to another user.")
                else:
                    issued_book = IssuedBook(
                        Barcode=barcode,
                        national_id=national_id,
                        user=user,
                        book=book
                    )
                    issued_book.save()
                    return redirect('profile')  # Adjust the URL pattern name as needed
            except Book.DoesNotExist:
                form.add_error('Barcode', "Book not found.")
            except Users.DoesNotExist:
                form.add_error('national_id', "User not found.")
    else:
        form = IssuedBookForm()

    return render(request, 'app/issuebook.html', {'form': form})



@login_required(login_url='/admin_login')
def viewissuebook_view(request):
    issued_books = IssuedBook.objects.select_related('user').all()

    context = {
        'issued_books': issued_books,
    }

    return render(request, 'app/viewissuebook.html', context)

@login_required(login_url='/admin_login')
# views.py
def scan_qr_code(request):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    data = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Define the region of interest (ROI) for the small frame
        height, width, _ = frame.shape
        roi_x, roi_y, roi_w, roi_h = width // 4, height // 4, width // 2, height // 2
        roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

        data, bbox, _ = detector.detectAndDecode(roi)
        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox)):
                pt1 = tuple(bbox[i][0] + [roi_x, roi_y])
                pt2 = tuple(bbox[(i+1) % len(bbox)][0] + [roi_x, roi_y])
                cv2.line(frame, pt1, pt2, color=(255, 0, 0), thickness=2)
            if data:
                break

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return JsonResponse({'data': data})
@login_required(login_url='/admin_login')
def scanner(request):
    return render(request, 'app/scanner.html')

@login_required(login_url='/admin_login')
def librarian_list(request):
    librarians = Librarian.objects.all()
    return render(request, 'app/librarian_list.html', {'librarians': librarians})


@login_required(login_url='/admin_login')
def add_librarian(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        librarian_form = LibrarianForm(request.POST)

        if user_form.is_valid() and librarian_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            librarian = librarian_form.save(commit=False)
            librarian.user = user
            librarian.save()

            return redirect('librarian_list')

    else:
        user_form = UserForm()
        librarian_form = LibrarianForm()

    return render(request, 'app/add_librarian.html', {
        'user_form': user_form,
        'librarian_form': librarian_form
    })

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_issued_book_info(request):
    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        if not national_id:
            return JsonResponse({'error': 'National ID is required'}, status=400)
        try:
            issued_book = IssuedBook.objects.get(national_id=national_id)
            students = Users.objects.all()
            bookims=Book.objects.all()
            book = issued_book.book
            for student in students:
                if not student.national_id_image:
                    student.national_id_image_url = ''  # Or use a placeholder image URL
                else:
                    student.national_id_image_url = student.national_id_image.url

            for bookim in bookims:
                if not bookim.Profile_pic:
                    bookim.Profile_pic_url = ''  # Or use a placeholder image URL
                else:
                    bookim.Profile_pic_url = bookim.Profile_pic.url

            response_data = {
                'book_title': book.Title,
                'book_image': bookim.Profile_pic_url,
                'issued_date': issued_book.issuedate,
                'expiry_date': issued_book.expirydate,
                'fine': issued_book.fine,
                'national_id_image': student.national_id_image_url
                
            }
            return JsonResponse(response_data)
        except IssuedBook.DoesNotExist:
            return JsonResponse({'error': 'No issued book found for this National ID'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



from .forms import ReturnBookForm
from .models import IssuedBook, ReturnBook

def returnbook_view(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['Barcode']
            national_id = form.cleaned_data['national_id']
            
            # Find the issued book
            try:
                
                issued_book = IssuedBook.objects.get(Barcode=barcode, national_id=national_id)
                
                # Move data to ReturnBook table
                ReturnBook.objects.create(
                    Barcode=issued_book.Barcode,
                    national_id=issued_book.national_id
                )
                
                # Delete from IssuedBook table
                issued_book.delete()

                return redirect('profile')  # Adjust the URL pattern name as needed
            except IssuedBook.DoesNotExist:
                form.add_error(None, "No matching issued book found.")

    else:
        form = ReturnBookForm()

    return render(request, 'app/returnbook.html', {'form': form})


def returnedbook_view(request):
    returned_books = ReturnBook.objects.all()  # Adjust this query to match your model
    context = {
        'returned_books': returned_books
    }
    return render(request, 'app/returnedbook.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Book

def view_book(request, id):
    # Get the book object by its ID or return a 404 error if not found
    book = get_object_or_404(Book, id=id)
    
    # Render a template with the book details
    return render(request, 'app/view_book.html', {'book': book})
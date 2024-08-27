from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signin', views.signin, name='signinpage'),
    path('logout', views.logoutUser, name='logout'),
    path('forgetpass', views.forgetpass, name='pass'),
    path('index', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path("addbook", views.addbook, name="addbook"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('signup', views.signup, name='signuppage'),
    path('viewbook', views.viewbook, name='viewbook'),
    path('core', views.core, name='core'),
    path('support', views.support, name='support'),
    path('view_student', views.view_student, name='view_student'),
    path('scanner/', views.scanner, name='scanner'),
    path('scan_qr_code/', views.scan_qr_code, name='scan_qr_code'),
    path('add_librarian/', views.add_librarian, name='add_librarian'),
    path('librarian_list/', views.librarian_list, name='librarian_list'),
    path('delete_student/<int:myid>/', views.delete_student, name='delete_student'),
    path('delete_book/<int:myid>/', views.delete_book, name='delete_book'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('issuebook/', views.issuebook_view),
    path('viewissuebook', views.viewissuebook_view, name='viewissuebook'),
    path('lms.png', RedirectView.as_view(url=staticfiles_storage.url('lms.png')),),
  
    path('scan_qr_code/', views.scan_qr_code, name='scan_qr_code'),
    path('get_issued_book_info/', views.get_issued_book_info, name='get_issued_book_info'),
    path('returnbook/', views.returnbook_view, name='returnbook'),
    path('returnedbooks/', views.returnedbook_view, name='returnedbooks'),
    path('view_book/<int:id>/', views.view_book, name='view_book'),
]



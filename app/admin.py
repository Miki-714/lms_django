from django.contrib import admin
from .models import *

admin.site.register(Book)
admin.site.register(Users)
admin.site.register(IssuedBook)
admin.site.register(Librarian)
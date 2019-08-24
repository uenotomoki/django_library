from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Member)
admin.site.register(Staff)
admin.site.register(Docindex)
admin.site.register(Doclist)
admin.site.register(Lendlist)
admin.site.register(Reservelist)
admin.site.register(Evaluation)
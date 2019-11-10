from django.contrib import admin
from account.models import Key, file_storage

# Register your models here.
admin.site.register(Key)
admin.site.register(file_storage)

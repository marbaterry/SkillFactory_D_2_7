from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(CategorySubscriber)

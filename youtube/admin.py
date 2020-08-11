from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Video

# Register your models here.
class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Video, MyModelAdmin)


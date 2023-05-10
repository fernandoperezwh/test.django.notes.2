# django packages
from django.contrib import admin
# local packages
from src.apps.nts_blogs.models import Blogs


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('folio', 'title', 'published')
    search_fields = ('folio', 'title',)
    list_filter = ('published',)

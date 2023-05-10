# django packages
from django.views.generic.list import ListView
# local packages
from src.apps.nts_blogs.models import Blogs


# Create your views here.
class BlogListView(ListView):
    model = Blogs
    template_name = "blogs_list_view.html"

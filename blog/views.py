from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse, Http404
from .models import Article, Category
from account.models import User
from account.mixins import AuthorAccessMixin
from datetime import datetime, timedelta
from django.db.models import Q


# Create your views here.


# def home(request):
#     return HttpResponse("hello, world")

# def home(request):
#     context = {
#         "username": "sajjad",
#         "age": 32,
#         "job": "Developer"
#     }
#     return render(request, 'blog/home.html', context)


# def home(request):
#     context = {
#         "articles": [
#             {
#                 "title": "هفت بازیساز در کورس آقای پاس لیگ برتر",
#                 "description": "با درخشش روز گذشته مسعود شجاعی در ترکیب تراکتور، حالا هفت بازیکن مدعی عنوان بهترین "
#                                "پاسور لیگ بیستم هستند.",
#                 "img": "https://static.farakav.com/files/pictures/thumb/01565459.jpg"
#             },
#             {
#                 "title": "مدعی دستکش طلا با بینی شکسته!(عکس)",
#                 "description": "سنگربان تراکتور در دوران حضور کوتاه خود در مقابل گل‌گهر سیرجان موفق شد دروازه‌اش را "
#                                "تنها 20 دقیقه نگه دارد و سپس به دلیل مصدومیت زمین را ترک کرد.",
#                 "img": "https://static.farakav.com/files/pictures/thumb/01565457.jpg"
#             },
#             {
#                 "title": "آینده صلاح باعث حواس‌پرتی لیورپول نیست",
#                 "description": "محمد صلاح، مهاجم مصری لیورپول، به تازگی راجع به رئال مادرید اظهارنظرات مثبتی کرده است "
#                                "و این موضوع شایعاتی را به وجود آورده است.",
#                 "img": "https://static.farakav.com/files/pictures/thumb/01565479.jpg",
#             }
#         ]
#
#     }
#     return render(request, 'blog/home.html', context)

# def home(request, page=1):
#     article_list = Article.objects.published().order_by('-publish')
#     paginator = Paginator(article_list, 2)
#     # page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         # "articles": Article.objects.all() # returns all articles
#         "articles": articles,  # returns published articles and orders by
#         # published date descending
#
#     }
#     return render(request, 'blog/home.html', context)


class ArticleList(ListView):
    # model = Article
    # context_object_name = 'articles'  # instead of using this line you can use object_list to get access to the context
    queryset = Article.objects.published()
    paginate_by = 2

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     last_month = datetime.today() - timedelta(days=30)
    #     context['popular_articles'] = Article.objects.published().annotate(
    #     count=Count('hits', filter=Q(articlehit__created__gt=last_month))).order_by('-count', '-publish')
    #     return context
    # template_name = 'blog/home.html'


# def detail(request, slug):
#     try:
#         article = Article.objects.get(slug=slug)
#     except Exception as e:
#         raise Http404
#     context = {"article": article}
#     return render(request, 'blog/detail.html', context)

# def detail(request, slug):
#     context = {
#         "article": get_object_or_404(Article.objects.published(), slug=slug)
#     }
#     return render(request, 'blog/detail.html', context)

class ArticleDetail(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)
        ip_address = self.request.user.ip_address

        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


#
# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 2)
#     # page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         "category": category,
#         "articles": articles,
#     }
#     return render(request, 'blog/category.html', context)


class CategoryList(ListView):
    paginate_by = 2
    template_name = "blog/category_list.html"

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 2
    template_name = "blog/author_list.html"

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        print(username)
        author = get_object_or_404(User, username=username)
        print(author.get_full_name())
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class SearchList(ListView):
    paginate_by = 2
    template_name = "blog/search_list.html"

    def get_queryset(self):
        search = self.request.GET.get('q')

        return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context


def api(request):
    data = {
        "1": {
            "title": "مقاله اول",
            "id": "20",
            "slug": "first article",

        },
        "2": {
            "title": "مقاله دوم",
            "id": "21",
            "slug": "second article",

        },
        "3": {
            "title": "مقاله سوم",
            "id": "22",
            "slug": "third article",

        },
    }
    return JsonResponse(data)

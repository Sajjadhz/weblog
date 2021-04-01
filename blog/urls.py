from django.urls import path
from .views import ArticleList, api, ArticleDetail, CategoryList, AuthorList, ArticlePreview, SearchList

app_name = "blog"  # best practice
urlpatterns = [
    path('home/', ArticleList.as_view(), name="home"),  # best practice
    path('home/page/<int:page>', ArticleList.as_view(), name="home"),  # best practice
    path('api/', api, name="api"),  # best practice
    path('article/<slug:slug>', ArticleDetail.as_view(), name="detail"),  # best practice
    path('preview/<int:pk>', ArticlePreview.as_view(), name="preview"),  # best practice
    path('category/<slug:slug>', CategoryList.as_view(), name="category"),  # best practice
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),  # best practice
    path('author/<slug:username>', AuthorList.as_view(), name="author"),  # best practice
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name="author"),  # best practice
    path('search/page/<int:page>', SearchList.as_view(), name="search"),  # best practice
    path('search/', SearchList.as_view(), name="search"),  # best practice
]

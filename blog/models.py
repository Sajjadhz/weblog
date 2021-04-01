from django.db import models
from django.utils import timezone
from extentions.utils import jalali_converter
from django.utils.html import format_html
# from django.contrib.auth.models import User
from account.models import User
from django.urls import reverse  # reverse converts string to the url
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# my managers, to read more about managers see https://docs.djangoproject.com/en/3.1/topics/db/managers/
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# Create your models here.
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندي')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندي')
    status = models.BooleanField(default=True, verbose_name='وضعیت نمايش')
    position = models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = 'دسته بندي'
        verbose_name_plural = 'دسته بندي ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()  # you need to include this property in your class while using model manager otherwise
    # you will get an error like that 'manager' object has no attribute ...


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # published
        ('i', 'در حال بررسی'),  # investigation
        ('b', 'برگشت داده شده'),  # back to revise
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles',
                               verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    category = models.ManyToManyField(Category, verbose_name='دسته بندي', related_name="articles")
    description = models.TextField(verbose_name='توضیحات')
    thumbnail = models.ImageField(upload_to="images", null=True, blank=True, verbose_name='تصویر')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='مقاله')
    updated = models.DateTimeField(auto_now=True, verbose_name='مقاله')
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits",
                                  verbose_name='بازدیدها')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:home")

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = "زمان انتشار"

    def category_published(self):
        return self.category.filter(status=True)

    def thumbnail_tag(self):  # this method will return html tag if thumbnail was already exist else will return '---'
        if self.thumbnail:
            return format_html(
                "<img width= 100 height= 75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))
        else:
            return '---'

    thumbnail_tag.short_description = "عکس"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.active()])

    category_to_str.short_description = "دسته بندی"

    objects = ArticleManager()  # you need to include this property in your class while using model manager otherwise you will get an error like that 'manager' object has no attribute ...


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

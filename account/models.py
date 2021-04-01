from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# best practice note: this is highly recommended to implement customized user tasks at the begging of project
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_author = models.BooleanField(default=False, verbose_name='وضعیت نویسندگی')
    special_user = models.DateTimeField(default=timezone.now, verbose_name='کاربر ویژه تا')

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    is_special_user.boolean = True  # with this line of codes django prints our bolean parameters as it's built-in parameters
    is_special_user.short_description = "وضعیت کاربر ویژه"

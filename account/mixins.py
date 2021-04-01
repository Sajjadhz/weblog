from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):  # this function is django built-in function
        self.fields = [
            'title', 'category', 'slug',
            'description', 'thumbnail', 'publish', 'is_special', 'status'
        ]
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):  # this function is django built-in function
        article = get_object_or_404(Article, pk=pk)  # it's very very important note to use object not list
        if article.author == request.user and article.status in ['b', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("account:profile")


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):  # this function is django built-in function
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("login")


class SuperuserAccessMixin():
    def dispatch(self, request, *args, **kwargs):  # this function is django built-in function

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404(" You can not see this page.")


class AuthorHasAccesss:
    # def get_queryset(self):
    #     if self.user.is_author or self.user.is_superuser:
    #         return super().get_queryset()
    #     else:
    #         return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        self.object = None
        if self.request.user.is_author or self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse(status=403)

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

User = settings.AUTH_USER_MODEL


class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):  # __icontains
        # qs = self.filter(title__iexact=query)
        # my_qs = self.filter(content__icontains=query)
        # qs = (qs|my_qs).distinct()
        # return qs

        # alternate
        lookup = (
            Q(title__iexact=query) |
            Q(content__icontains=query) |
            Q(slug__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
            )
        return self.filter(lookup)


class BlogPostManager(models.Manager):
    # def published(self):
    #     now = timezone.now()
    #     # get_queryset() ~ BlogPost.objects
    #     return self.get_queryset().filter(publish_date__lte=now)
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()  # will work without all()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


# Create your models here.
class BlogPost(models.Model):  # blogpost_set : lowercase model name and use [foriegn key]
    # user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)     # on_delete will delete the data related to the user
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # hello world -> hello-world (string url)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # auto_add_now is the time when post is added to database
    updated = models.DateTimeField(auto_now=True)  # auto_now adds the time whenever you update or hit save button

    objects = BlogPostManager()

    class Meta:  # sorting server content
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):  # for navigation purpose
        return f"/blog/{self.slug}"  # alt for navigation on list.html

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        # return f"/blog/{self.slug}/delete"
        return f"{self.get_absolute_url()}/delete"

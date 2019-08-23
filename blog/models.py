from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class BlogPost(models.Model):  # blogpost_set : lowercase model name and use [foriegn kry]
    # user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)     # on_delete will delete the data related to the user
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # hello world -> hello-world (string url)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) # auto_add_now is the time when post is added to database
    updated = models.DateTimeField(auto_now=True)   # auto_now adds the time whenever you update or hit save button

    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):  # for navigation purpose
        return f"/blog/{self.slug}"  # alt for navigation on list.html

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        # return f"/blog/{self.slug}/delete"
        return f"{self.get_absolute_url()}/delete"

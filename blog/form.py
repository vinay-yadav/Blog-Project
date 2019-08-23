from django import forms
from .models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)


class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date']

    def clean_title(self, *args, **kwargs):
        # print(dir(self))
        instance = self.instance
        # print(instance)
        title = self.cleaned_data.get('title')
        # print(title)
        # qs = BlogPost.objects.filter(title=title) # filter for title(exact)
        qs = BlogPost.objects.filter(title__iexact=title)   # filter fot title for both capital and small
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)     # id = instance.id
        if qs.exists():
            raise forms.ValidationError('This title has already been used')
        return title


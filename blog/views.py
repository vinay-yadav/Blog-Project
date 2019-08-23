from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404  # to handle URL errors
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

# Create your views here.
from .models import BlogPost
from .form import BlogPostForm, BlogPostModelForm


# def blog_post_details_page(request, blog_id):             # dynamic url with id
#     # Simple error handling
#     # try:
#     #     obj = BlogPost.objects.get(id=blog_id)
#     # except:
#     #     raise Http404
#     print(blog_id.__class__)
#
#     # more specfic type of error
#     # try:
#     #     obj = BlogPost.objects.get(id=blog_id)
#     # except BlogPost.DoesNotExist:
#     #     raise Http404
#     # except ValueError:
#     #     raise Http404
#
#     obj = get_object_or_404(BlogPost, id = blog_id)
#     template_name = "details.html"
#     context = {"object": obj}
#     return render(request, template_name, context)

# GET -> for 1 object
# FILTER -> for list [] of objects

# def blog_post_details_page(request, slug):
#     print("Django Says", request.method, request.user, request.path)
#     # obj = BlogPost.objects.get(slug=slug)
#     # query_set = BlogPost.objects.filter(slug=slug)
#     # print(query_set.count())
#     # print(query_set.__class__)
#     # # if query_set.count() >= 1:
#     # #     obj = query_set.first()
#     # if query_set.count() == 0:
#     #     raise Http404
#     # obj = query_set.first()
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = "details.html"
#     context = {"object": obj}
#     return render(request, template_name, context)

def blog_post_list_view(request):
    # list out objects
    # could be search
    now = timezone.now()
    qs = BlogPost.objects.all()
    qs = BlogPost.objects.filter(publish_date__lte = now)   # gte -> greater than equal to & lte -> less than equal to
    template_name = "blog/list.html"
    context = {'objects_list': qs}
    return render(request, template_name, context)


# @login_required
@staff_member_required
def blog_post_create_view(request):
    # create objects
    # wil create objects using form
    # form = BlogPostForm(request.POST or None)
    form = BlogPostModelForm(request.POST or None)
    if form.is_valid():
        # print(form.cleaned_data)
        # # title = form.cleaned_data['title']
        # # obj = BlogPost.objects.create(title=title)        # for data one at a time
        # obj = BlogPost.objects.create(**form.cleaned_data)  # it take dictionary and unpack at DB using fields

        # manipulating data and then saving
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + '_manipulated'
        obj.user = request.user  # set data for logged user otherwise will set to default user
        obj.save()

        # saving data direct from form using ModelForm
        # form.save()
        form = BlogPostForm()
    template_name = "form.html"
    context = {'form': form}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    print("Django Says", request.method, request.user, request.path)
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/details.html"
    context = {"object": obj}
    return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = "form.html"
    context = {'form': form, 'title': f"Update {obj.title}"}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/delete.html"
    if request.method == 'POST':
        obj.delete()
        return redirect('/blog')
    context = {"object": obj}
    return render(request, template_name, context)

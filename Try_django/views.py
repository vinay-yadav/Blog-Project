from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .form import ContactForm

from blog.models import BlogPost


# Don't Repeat Yourself (DRY)

def home_page(request):
    # my_title = "Hello there...."
    # # doc = "<h1>{{title}}</h1>".format(title = my_title)   #django use double curly brackets({{}})
    # return render(request, "hey_there.html", {"title":my_title})
    my_title = "Welcome to Try Django"
    qs = BlogPost.objects.all()[:5]
    context = {'title': my_title, 'blog_list': qs}
    # if request.user.is_authenticated:
    #     context = {"title": my_title, "my_list": [1, 2, 3, 4, 5]}
    return render(request, "home.html", context)


def about_page(request):
    return render(request, "about.html", {"title": "About Us"})


def contact_page(request):
    # print(request.POST)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()  # refreshing data otherwise form.html will have same data every time
    context = {
        'title': 'Contact Us',
        'form': form
    }
    return render(request, "form.html", context)


def example_page(request):  # using HttpResponse to render an html file
    context = {"title": "Examples"}
    template_name = "hey_there.html"
    template_obj = get_template(template_name)
    rendered_item = template_obj.render(context)
    return HttpResponse(rendered_item)

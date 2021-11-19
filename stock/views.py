from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import render
from django.http import HttpResponse
from stock.models import Category
from stock.models import Page
from stock.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse
from stock.forms import UserForm, UserProfileForm


# Create your views here.
def index(request):
    category_list=Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:4]
    context_dict={}
    #context_dict['boldmessage']:' hi, julia '
    context_dict['categories']=category_list
    context_dict['pages']=page_list
    return render(request,'stock/index.html', context=context_dict)

def about(request):
    print(request.method)
    print(request.user)
    return render(request,'stock/about.html')


def show_category(request,category_name_slug):
    context_dict={}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages']=pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['pages']=None
        context_dict['category']=None

    return render(request,'stock/category.html',context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method =='POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/stock/')
        else:
            print(form.errors)
    return render(request,'stock/add_category.html',{'form':form})


def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect('/stock/')

    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('stock:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict={'form':form,'category':category}
    return render(request,'stock/add_page.html',context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered= True
        else:
            print(user_form.errors,profile_form.errors)
    else:
            user_form = UserForm() 
            profile_form = UserProfileForm() 

    return render(request,'stock/register.html',
                     context = {'user_form':user_form,
                       'profile_form':profile_form,
                       'registered':registered})


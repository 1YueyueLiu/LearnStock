from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import render
from django.http import HttpResponse
from stock.bing_search import run_query
from stock.models import Category
from stock.models import Page,Comment
from stock.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse
from stock.forms import UserForm, UserProfileForm,CommentForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User 
from stock.models import UserProfile
from django.utils.decorators import method_decorator
from django.views import View


# Create your views here.

# the view of cookie
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if(datetime.now() - last_visit_time).days > 0 :
        visits= visits+1
        request.session['last_visit']=str(datetime.now())
    else:
        request.session['last_visit']=last_visit_cookie
    request.session['visits'] =visits

# the view of homepage
def index(request):
    category_list=Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:4]
    context_dict={}
    #context_dict['boldmessage']:' hi, julia '
    context_dict['categories']=category_list
    context_dict['pages']=page_list
    
    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']

    response = render(request,'stock/index.html',context=context_dict)
    
    return response
    

def about(request):
    #context_dict = {}
    #visitor_cookie_handler(request)
    #context_dict['visits']= request.session['visits']
    
    #print(request.method)
    #print(request.user)
    #if request.session.test_cookie_worked():
     #   print("TEST COOKIE WORKED!")
      #  request.session.delete_test_cookie()

    return render(request,'stock/about.html')


# the view of show the category
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
    form = CommentForm()
    context_dict['form']=form
        
    
    try:
        comment = Comment.objects.filter(category=category_name_slug).order_by('-posttime')[:6]
        context_dict['comments'] = comment
    except Comment.DoesNotExist:
        context_dict['comments'] = None
    
    return render(request,'stock/category.html',context=context_dict)

# the view of function add new category
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method =='POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            this_category=form.save(commit=True)
            this_category.views=0
            this_category.likes=0
            this_category.save()
            print(this_category)

            return redirect('stock:News')
        else:
            print(form.errors)
    return render(request,'stock/add_category.html',{'form':form})

# the view of function add new page
@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect('/index/')

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


#def register(request):
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

#def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details:{username},{password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'stock/login.html')

# the view of simuilator page, has a login required
@login_required
def restricted(request):
    return render(request,'stock/restricted.html')

@login_required
#def user_logout(request):
 #   logout(request)
  #  return redirect(reverse('stock:index'))





def goto_url(request):
    if request.method == 'GET':
            page_id = request.GET.get('page_id')

            try:
                selected_page = Page.objects.get(id=page_id)
            except Page.DoesNotExist:
                return redirect(reverse('stock:index'))

            selected_page.views = selected_page.views + 1
            selected_page.save()
            

            return redirect(selected_page.url)
          
    return redirect(reverse('stock:index'))


@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('index'))
        else:
            print(form.errors)
    context_dict={'forms':form}
    return render(request,'stock/profile_registration.html',context_dict)

# the view of news page
def News(request):
    category_list=Category.objects.order_by('-likes')
    page_list=Page.objects.order_by('-views')
    context_dict={}
    #context_dict['boldmessage']:' hi, julia '
    context_dict['categories']=category_list
    context_dict['pages']=page_list

    
    return render(request,'stock/News.html',context=context_dict)

      
# the view of add comment
def add_comment(request, category_name_slug):
    form = CommentForm(request.POST)
    if form.is_valid() and form['content'] != None:
        f = form.save(commit=False)
        f.username = get_server_side_cookie(request, 'username', 'Anonym')
        f.username = request.user.username # temporary solution for comment username
        f.posttime = datetime.now()
        f.category = category_name_slug
        f.save()

        # for redirect back to the page after refresh
        return redirect(f'/stock/category/{category_name_slug}')
    else:
        print(form.errors)


  

#class AboutView(View):
    def get(self,request):
        context_dict={}

        visitor_cookie_handler(request)
        context_dict['visits']=request.session['visits']

        return render(request,'stock/about.html',context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
           user = User.objects.get(username=username)
        except User.DoesNotExist: 
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture}) 
        return (user, user_profile, form)

    @method_decorator(login_required) 
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('stock:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'stock/profile.html', context_dict)

    @method_decorator(login_required) 
    def post(self, request, username):
       try:
        (user, user_profile, form) = self.get_user_details(username)
       except TypeError:
        return redirect(reverse('stock:index'))
       form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

       if form.is_valid():
        form.save(commit=True)
        return redirect('stock:profile', user.username)
       else: 
        print(form.errors)
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'stock/profile.html', context_dict)



# the view of function search
def search(request):
    result_list=[]
    query = ''
    if request.method =='POST':
        query = request.POST['query'].strip()

        if query:
            result_list= run_query(query)
    return render(request,'stock/search.html',{'result_list':result_list})  
    
    
class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']
        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        category.likes = category.likes + 1
        category.save()
        return HttpResponse(category.likes)
        


from django import forms
from stock.models import Page,Category, UserProfile
from django.contrib.auth.models import User
from stock.models import Comment

# the form for category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text=" please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model= Category
        fields=('name',)

# the form for page
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="please enter the title of page.")
    url = forms.URLField(max_length=200,
                            help_text="please enter the URL of the page.")
    views = forms.IntegerField(widget= forms.HiddenInput(),initial=0)

    class Meta:
        model = Page
        exclude=('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url']=url

        return cleaned_data

# the form for user
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

# the form for userprofile
class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ('website','picture',)

# the form for comment
class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500)
    class Meta:
        model = Comment
        fields = ('content',)



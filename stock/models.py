from django.db import models
from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
# category model
class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)
        

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# page model
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# userprofile model
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username

# comment model     
class Comment(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    username = models.CharField(max_length=12)
    content = models.CharField(max_length=128)
    posttime = models.DateTimeField(default = datetime.now())
    category = models.SlugField()

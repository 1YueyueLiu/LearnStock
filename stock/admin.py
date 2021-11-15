from django.contrib import admin
from stock.models import Category,Page

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')

admin.site.register(Category)
admin.site.register(Page,PageAdmin)
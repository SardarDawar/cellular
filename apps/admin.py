from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Mobile Admin'
    site_title  = 'Mobile '
    index_title = 'Mobile '
 
my_admin_site = MyAdminSite(name='Mobile')

class profileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'contactNumber']
    search_fields = ['id', 'user__username', 'user__first_name', 'user__last_name', ]

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Name',)}


class planAdmin(admin.ModelAdmin):
    list_display = ['user','family_name', 'plan_name']

class subscriptionAdmin(admin.ModelAdmin):
    list_display = ['user','plan', 'created_at']

my_admin_site.register(Group, GroupAdmin)
my_admin_site.register(User, UserAdmin)
my_admin_site.register(profileModel, profileAdmin)

my_admin_site.register(category, categoryAdmin)
my_admin_site.register(plan, planAdmin)
my_admin_site.register(subscription, subscriptionAdmin)
from django.contrib import admin

# Register your models here.

from .models import *

#admin.site.register(Company)
#admin.site.register(Agent)
#admin.site.register(Customer)
"""
class ProductivityAdmin(admin.ModelAdmin):
    list_display = ['agent','date','productivity_type','value']
    list_filter = ['date']
admin.site.register(Productivity,ProductivityAdmin)

#admin.site.register(Productivity)
#admin.site.register(Norm)
#admin.site.register(Project)
#admin.site.register(SubProject)

class AdressAdmin(admin.ModelAdmin):
    list_display = ['street','area','land_mark','state','country','zipcode']
admin.site.register(Adress,AdressAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name','adress']
admin.site.register(Company,CompanyAdmin)
"""

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name','agent','customer']
admin.site.register(Project,ProjectAdmin)

"""
class SubProjectAdmin(admin.ModelAdmin):
    list_display = ['sub_project_name','project_name','sub_project_target']
admin.site.register(SubProject,SubProjectAdmin)

"""

class AgentAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Agent,AgentAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Customer,CustomerAdmin)

"""
class NormAdmin(admin.ModelAdmin):
    list_display = ['company','per_day']
admin.site.register(Norm,NormAdmin)
"""

class RawtableAdmin(admin.ModelAdmin):
    list_display = ['project','employee','volume_type','per_day','per_hour','norm','date','created_at','modified_at']
admin.site.register(RawTable,RawtableAdmin)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class UserCreationFormExtended(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super(UserCreationFormExtended, self).__init__(*args, **kwargs) 
        self.fields['first_name'] = forms.CharField(label=_("First Name"), max_length=30)
        self.fields['last_name'] = forms.CharField(label=_("Last Name"), max_length=30)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)

UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
    }),
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


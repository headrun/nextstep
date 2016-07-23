from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""
class Adress(models.Model):
    street   = models.CharField(max_length=255)
    area     = models.CharField(max_length=255)
    land_mark= models.CharField(max_length=255)
    state    = models.CharField(max_length=255)
    country  = models.CharField(max_length=255)
    zipcode  = models.IntegerField(max_length=255, default=0)

    class Meta:
        db_table = u'adress'
    def __unicode__(self):
        return self.area

class Company(models.Model):
    name   = models.CharField(max_length=255)
    adress = models.ForeignKey(Adress, null=True)

    class Meta:
        db_table = u'company'
    def __unicode__(self):
        return self.name


class SubProject(models.Model):
    sub_project_name  = models.CharField(max_length=255)
    project_name      = models.ForeignKey(Project, null=True)
    sub_project_target= models.IntegerField(max_length=255, default=0)

    class Meta:
        db_table = u'sub_project'
    def __unicode__(self):
        return self.sub_project_name
"""
class Agent(models.Model):
    name        = models.ForeignKey(User, null=True)
    #company     = models.ForeignKey(Company, null=True)
    #sub_project = models.ForeignKey(SubProject, null=True)

    class Meta:
        db_table = u'agent'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

class Customer(models.Model):
    #company = models.ForeignKey(Company, null=True)
    name    = models.ForeignKey(User, null=True)

    class Meta:
        db_table = u'customer'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

"""
class Productivity(models.Model):
    #volume_type = models.CharField()
    agent     = models.ForeignKey(Agent, null=True)
    CHOICE = (
        ('1','per_day'),
        ('2','per_hour'),
        ('3','per_week'),
        ('4','per_month')
    )
    productivity_type = models.CharField(max_length=20,choices=CHOICE, default='per_day')
    value = models.IntegerField(max_length=255, default=0)
    #per_day   = models.IntegerField(max_length=255, default=0)
    #per_hour  = models.IntegerField(max_length=255, default=0)
    #per_week  = models.IntegerField(max_length=255, default=0)
    #per_month = models.IntegerField(max_length=255, default=0)
    date    = models.DateTimeField()

    class Meta:
        db_table = u'productivity'
        unique_together = (("agent","date"),)
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.agent_id).values_list('username',flat=True)
        return user_obj[0]

class Norm(models.Model):
    company = models.ForeignKey(Company, null=True)
    per_day = models.IntegerField(max_length=255, default=0)

    class Meta:
        db_table = u'norm'
    def __unicode__(self):
        return str(self.per_day)
"""
class Project(models.Model):
    project_name    = models.CharField(max_length=255)
    agent = models.ForeignKey(Agent, null=True)
    customer = models.ForeignKey(Customer, null=True)

    class Meta:
        db_table = u'project'
    def __unicode__(self):
        return self.project_name


class RawTable(models.Model):
    #project     = models.CharField(max_length=255, default='')
    project     = models.ForeignKey(Project, null=True)
    #person_usename = Project.objects.filter(id=)
    #user        = models.ForeignKey(User, null=True)
    employee    = models.CharField(max_length=255, default='')
    volume_type = models.CharField(max_length=255, default='')
    per_hour    = models.IntegerField(max_length=255, default=0)
    per_day     = models.IntegerField(max_length=255, default=0)
    date        = models.DateTimeField()
    norm        = models.IntegerField(max_length=255, default=0)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        db_table = u'raw_table'
        unique_together = (("date","employee"),)


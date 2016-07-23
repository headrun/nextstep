from django.conf.urls import include, url 
from django.contrib import admin

urlpatterns = [ 
    # Examples:
    url(r'^person','dashboard.views.persons_last_week_stats', name="persons_last_week_stats"),
    url(r'^stats','dashboard.views.last_week_stats', name="last_week_stats"),
    url(r'^elaborate','dashboard.views.last_week_stats_elaborate', name="last_week_stats_elaborate"),
    #url(r'^user_wise','dashboard.views.user_wise', name="user_wise"),
    url(r'^board','dashboard.views.dashboard_insert', name="dashboard_insert"),
    url(r'^dashboard','dashboard.views.dashboard', name="dashboard"),
    url(r'^upload/','dashboard.views.upload', name="upload"),
]

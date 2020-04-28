from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    url(r'^$',views.home, name = "home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name= "logout"),

    #----------------------------------------------------------------------------
    url(r'^profile/(?P<user_name>\w+)/$', views.profile_user, name= "profile"),
    #---------------------------------------------------------------------------
    url(r'^register/$', views.register_user, name= "register"),
    url(r'^edit_profile/$', views.edit_profile, name = "edit_profile"),
    
    
    # ****************************************************************
    # User Dashboard
    # ****************************************************************
    url(r'^dashbaord/$', views.dashboard, name = "dashboard"),
    
    #Password Change URL............
    url(r'^change_password/$', views.change_password, name = "change_password"),

    #password Reset URLS...........
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Email Confirm URLs.....
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

    #Contact Us Page ...
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^search/$', views.search, name="search"),
    ######### Plans ##################
    url(r'^plan/$', views.planList, name="plan"),
    url(r'^plandetail/(?P<id>\d+)/$', views.plandetail, name="plandetail"),
    url(r'^planform/$', views.planFormView, name="planform"),
    url(r'^planeditform/(?P<id>\d+)/$', views.planEditFormView, name="planeditform"),
    url(r'^delete/(?P<id>\d+)/$', views.delete_view,name='delete' ), 

    # ****************************************************************
    # Calculator Page
    # ****************************************************************
    path('calculator', views.CalculatorView, name="Calculator"),
    
    # ****************************************************************
    # Plan Join Page
    # ****************************************************************
    path('join-plan/<int:category_id>/<int:plan_id>/', views.Join_A_Plan, name="Join"),
    
    # ****************************************************************
    # Subscription Cancel
    # ****************************************************************
    path('cancel-subscription/<int:plan_id>/<int:sub_id>/', views.Cancel_A_Plan, name="cancel"),
    
    # ****************************************************************
    # User plans
    # ****************************************************************
    path('user-plans', views.Plans, name="Plans"),
    
    # ****************************************************************
    # Approve a subscription for a user
    # ****************************************************************
    path('approve-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.ApproveSubscription, name="Approve"),

    # ****************************************************************
    # Disapprove a subscription for a user
    # ****************************************************************
    path('disapprove-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.DisapproveSubscription, name="Disapprove"),

    # ****************************************************************
    # Edit a subscription
    # ****************************************************************
    path("edit-a-subscription/<int:plan_id>/<int:sub_id>/", views.EditSubscription, name="EditSubscription"),
    
    # ****************************************************************
    # Subscription Detail View
    # ****************************************************************
    path('detail-view-subscription/<int:plan_id>/<int:sub_id>', views.Detail, name="Details"),

    # ****************************************************************
    # Device Campatibility
    # ****************************************************************
    path('confirm-reservation', views.deviceCompatibility, name="Reservation"),
]
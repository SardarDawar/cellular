from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

class profileModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    contactNumber = models.IntegerField(blank = True, null=True, default=0)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
    class Meta:
        verbose_name = 'Profile'
        
    def get_contact(self):
        return self.contactNumber


class category(models.Model):
    Name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150)

    def __str__(self):
        return self.Name
    
     # ****************************************************************
     # Get all plans for a specific category
     # ****************************************************************
    def get_plans(self):
        return self.plan_set.all().order_by('-number_of_open_slots')




class plan(models.Model):
    user                                  = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)                                                
    category                              = models.ForeignKey(category, on_delete= models.CASCADE)                                                
    family_name                           = models.CharField(max_length=150)
    plan_name                             = models.CharField(max_length=150)
    number_of_open_slots                  = models.IntegerField(blank=False, default=0, null=False)       
    monthly_payment_date                  = models.CharField(max_length=150)
    currently_monthly_payment_per_line    = models.CharField(max_length=150)
    total_slots = models.IntegerField(verbose_name="Total Fixed Slots", blank=False, null=False, default=0)
    linkWeb = models.URLField(max_length = 200, blank=True, default='', null=True)
    notes = models.TextField(max_length = 500, blank=True, default ='', null = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_name
    
    # ****************************************************************
    # Get Category ID
    # ****************************************************************
    def get_category_id(self):
        return category.objects.get(id=self.category.id).id
    
    
    # ****************************************************************
    # Get Plan Owner Contact Number
    # ****************************************************************
    def get_contact(self):
        try:
            return profileModel.objects.get(user=User.objects.get(username = self.user.username)).contactNumber
        except:
            return None
    
    # ****************************************************************
    # Subscription Objects 
    # ****************************************************************
    def get_subscription_objects(self):
        return self.subscription_set.all()
    
    # ****************************************************************
    # Retrieve Plan Subscription status 
    # ****************************************************************
    def get_approve_subscription(self):
        try:
            return subscription.objects.get(user = User.objects.get(username = self.user.username), plan__id =  self.id )
        except:
            return  None
        
    # ****************************************************************
    # Retrive whether the current plan have available slots to subscribe
    # ****************************************************************
    def get_available_status(self):
        try:
            if int(self.number_of_open_slots) > 0:
                return True
            else:
                return False
        except Exception as e:
            return self.number_of_open_slots

    # ****************************************************************
    # Retrive the Subscription model for current login user and plan
    # ****************************************************************
    def get_subscription(self):
        try:
            return subscription.objects.get(user = User.objects.get(username = self.user.username), plan__id =  self.id )
        except:
            return None

class subscription(models.Model):
    user                                  = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)                                                
    plan                                  = models.ForeignKey(plan, on_delete= models.CASCADE) 
    number_of_slots = models.IntegerField(verbose_name="Number of Slots",
                                          blank=False,
                                          null = False,
                                          default = 0)
    TotalAmount = models.IntegerField(verbose_name = "Total Amount",
                                      blank = False,
                                      null = False,
                                      default = 0)
     
    created_at                            = models.DateField(auto_now_add=True)  

    approved = models.BooleanField(blank=False, null =False, default=False)

    def __str__(self):
        return f"{self.user.username}'s Subscription"                                           

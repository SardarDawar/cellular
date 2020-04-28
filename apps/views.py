from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from django.urls import reverse
from django.db.models import Q

#################################################################################
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(api_key='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')
from_email = Email("futuresoftcode@gmail.com")


from .models import profileModel, category

##################################################################################

def handler404(request):
    return render(request, '404.html', status=404)

def home(request):
    form = planForm()
    error= None
    if request.method == "POST":
        form= planForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user=request.user
            new.number_of_open_slots = new.total_slots
            new.save()
            form.save()
        else:
            error  =True
    value=plan.objects.all()
    if request.GET.get("category"):
        if request.GET.get("category") == "All":
            categories = category.objects.all()
        else:    
            categories = category.objects.filter(Name = request.GET['category'])
    else:
        categories = category.objects.all()
    # print(categories)
    return render(request, 'music/home.html',{'value':value, 'categories': categories,  'form':form, 'error' : error, 'filters': category.objects.all()} )

# ****************************************************************
# User Dashboard
# ****************************************************************
@login_required()
def dashboard(request):
    obj = subscription.objects.filter(
        user = User.objects.get(username=request.user.username)
    ).order_by('number_of_slots')
    context={
        'obj' : obj
    }
    return render(request, 'music/dashboard.html', context)

def login_user(request):
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    return render(request, 'music/login.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required()
def profile_user(request, user_name):
    message = ''
    try:
        user = User.objects.get(username = user_name)
        editProfile = False
        #print(request.user.username == user_name)
        if (request.user==user):
            if request.user.is_superuser:
                contactNumber = None
                editProfile = True
            else:
                contactNumber  = profileModel.objects.get(user = user).contactNumber
                editProfile = True
        else:
            if request.user.is_superuser:
                contactNumber  = profileModel.objects.get(user = user).contactNumber
                editProfile = False
            else:
                contactNumber = None
                editProfile = None
    except:
        user=request.user
        if request.user.is_superuser:
            contactNumber = None
            editProfile = True
            message = user_name + " Doest Not Exists "
        else:
            contactNumber  = profileModel.objects.get(user = User.objects.get(username = request.user.username)).contactNumber
            editProfile = True
            message = user_name
    return render(request, 'music/profile.html', {'contactNumber': contactNumber,'editProfile' :editProfile, 'user':user, 'message' : message})
    
def register_user(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email'].lower()
            user.save()
            profile = profileModel.objects.create(user = user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.save()
            current_site = get_current_site(request)
            content = render_to_string('music/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            subject = 'Activate your account.'
            to_email = (form.cleaned_data.get('email'))
            ################################
            # to_email = To(form.cleaned_data.get('email').lower())
            subject = 'Activate your account.'
            # mail = Mail(from_email, to_email, subject, content)
            # sg.client.mail.send.post(request_body=mail.get())
            email = EmailMessage(subject, content, to=[to_email])
            email.send()
            return render(request, 'music/acc_active_email_confirm.html')
    return render(request, 'music/register.html', {'form' : form, 'form_2' : form_2})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required()
def edit_profile(request):
    try:
        profile = profileModel.objects.get(user=request.user)
    except profileModel.DoesNotExist :
        profile = profileModel.objects.create(user=request.user)
        profile.save()
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
        form_2 = profileInformForm(instance=profile)
    else:
        # print(request.POST)
        form_2 = profileInformForm(request.POST,instance=profile)
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid() and form_2.is_valid():
            form.save()
            form_2.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    return render(request, 'music/edit_profile.html',{'form' : form, 'profile':profile, 'form_2':form_2})

@login_required()
def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    return render(request, 'music/change_password.html' , {'form': form})

def contact(request):
    if request.method!='POST':
        form = contactForm()
    else:
        form = contactForm(request.POST)
        if form.is_valid():
            mail_subject = 'Contact -- By -- ' + form.cleaned_data.get('userName')
            to_email = settings.EMAIL_HOST_USER
            message = form.cleaned_data.get('body')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('home')
    
    context= {'form' : form}
    return render(request, 'music/contact.html', context)


def search(request):

    query = request.GET.get('query', None)
    search_user = profileModel.objects.all()
    if query is not None:
        search_user = search_user.filter(
            Q(user__username__icontains=query) |
            Q(contactNumber__icontains=query) 
    

        )
    # print(query)
    # for i in search_user:
    #     print(i.user.email)
    context = {

        'search_user': search_user,
        'query':query
     
    }

    return render(request, 'music/search.html', context)


# ****************************************************************
# Add a New Plan Form
# ****************************************************************
def planFormView(request):
    form   =    planForm()
    if request.method== 'POST':
        form= planForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user=request.user
            new.number_of_open_slots = new.total_slots
            new.save()
            form.save()
            return redirect('dashboard')
    context = {
        'form':form,
    }
    return render(request,'app/form_plan.html',context)

@login_required
def planEditFormView(request,id):
    try:
        obj    =    plan.objects.get(id=id)
        if obj.user == User.objects.get(username = request.user.username):
            form   =    planForm(instance=obj)
            if request.method== 'POST':
                form= planForm(request.POST,instance=obj)
                if form.is_valid():
                    new = form.save(commit=False)
                    new.user=request.user
                    new.save()
                    form.save()
                    messages.success(request, "Plan has been edited successfully.")
                    return redirect('plan')
            context = {
                'form':form,
                'object':obj,
            }
            return render(request,'app/form_edit_plan.html',context)
        else:
            messages.success(request, "Does Not have access.")
            return render(request, 'app/error.html')
    except:
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')

def planList(request):
    plans  = plan.objects.filter(user=request.user)
     
    context = {
        'plans':plans
    }

    return render(request,'app/list_plan.html',context)

def plandetail(request,id):
    obj    =    plan.objects.get(id=id)

    context = {
        'obj':obj,
    }
    return render(request,'app/plan_detail.html',context)


def delete_view(request, id): 
    context ={} 
    obj = plan.objects.get( id = id) 
  
    if request.method =="POST": 
        obj.delete() 
        return redirect("dashboard") 
  
    return render(request, "app/delete_view.html", context) 



    
# ****************************************************************
# Calculator
# ****************************************************************
@login_required
def CalculatorView(request):
    if request.method == "POST":
        print(request.POST)
    template_name = "app/calculator.html"
    return render(request, template_name, context = {})



# ****************************************************************
# Join A Subscription (Join Plan)
# ****************************************************************
@login_required
def Join_A_Plan(request, category_id, plan_id):
    try:
        c = category.objects.get(id = category_id)
        p = plan.objects.get(id = plan_id, category = c)
        if request.method == "POST":
            try:
                obj, status = subscription.objects.get_or_create(
                    user=User.objects.get(
                        username=request.user.username
                    ),
                    plan = p
                )
                if status:
                    obj.number_of_slots = request.POST['number_of_slots']
                    obj.TotalAmount = int(p.currently_monthly_payment_per_line) * int(request.POST['number_of_slots'])
                    obj.save()
                    # Reduced the plan available slots for subscription
                    p.number_of_open_slots = int(p.number_of_open_slots)- int(request.POST['number_of_slots'])
                    p.save()
                    # ****************************************************************
                    # Email Settings
                    # mail = Mail(from_email, to_email, subject, content)
                    # sg.client.mail.send.post(request_body=mail.get())
                    # ****************************************************************
                    current_site = get_current_site(request)
                    link_build = str(request.scheme) + "://" + str(current_site.domain) +  str(reverse("Details", args=[ plan_id, obj.id ]))
                    to_email = (p.user.email)
                    subject = 'Subscription Alert'
                    content = f"A Subscription has been added to your plan.Kindly visit the following link to see details.\n\t{link_build}"
                    email = EmailMessage(subject, content, to=[to_email])
                    email.send()
                    messages.success(request, "Account Owner has been notified about your subscription to this plan. Thanks")
                    return redirect(reverse("Join", args=[category_id,plan_id]))
                else:
                    messages.success(request, "You have already been subscribed to this plan. Thanks")
                    return redirect(reverse("Join", args=[category_id,plan_id]))
            except Exception as e:
                print(e)
                messages.success(request, "Due to some technical reasons, subscription can not be done right now. Sorry")
                return redirect(reverse("Join", args=[category_id,plan_id]))
        template_name= "app/join.html"
        p = plan.objects.get(id = plan_id)
        slots = p.number_of_open_slots
        slots = [i for i in range(1, (slots) + 1)]
        context= {
            'slots' : slots,
            'plan': p,
            'total' : len(slots)
        }
        return render(request, template_name, context )
    except (plan.DoesNotExist, category.DoesNotExist):
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')



# ****************************************************************
# Calcel A Subscription (Joined Plan)
# ****************************************************************
@login_required
def Cancel_A_Plan(request,  plan_id, sub_id ):
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(id = sub_id, plan = p, user=User.objects.get(username=request.user.username))
        try:
            # ****************************************************************
            # Email Settings
            # to_email = To(p.user.email)
            # mail = Mail(from_email, to_email, subject, content)
            # sg.client.mail.send.post(request_body=mail.get())
            # current_site = get_current_site(request)
            # ****************************************************************
            subject = 'Subscription Alert'
            content = f"""A Subscription has been removed to your plan.\n
                    Following are the subscription details\n
                    Subscription user: {s.user}\n
                    Subscription Plan: {s.plan.plan_name}\n
                    Subscription Number of Slots: {s.number_of_slots}\n
                    Subscription Total Amount: {s.TotalAmount}\n 
                    Subscription Timestamp: {s.created_at}"""
            to_email = (p.user.email)
            email = EmailMessage(subject, content, to=[to_email])
            p.number_of_open_slots  = int(p.number_of_open_slots) + int(s.number_of_slots)
            p.save()
            s.delete()
            email.send()
            messages.success(request, "Your subscription has been cancelled and Account owner has ben notified about it. You can re-subscribe it anytime later.")
            return redirect("dashboard")
        except:
            messages.success(request, "Due to some technical reasons, subscription can not be done right now. Sorry.")
            return redirect("dashboard")
    except (subscription.DoesNotExist, plan.DoesNotExist) as e:
        # print(e)/
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    except Exception as e :
        # print(e)
        messages.success(request, "Due to some technical reasons, subscription can not be done right now. Sorry.")
        return redirect("dashboard")
    
# ****************************************************************
# User Added Plans
# ****************************************************************
@login_required
def Plans(request):
    obj=plan.objects.filter(user=User.objects.get(username=request.user.username))
    categories = category.objects.all()
    A = []
    C = {}
    for i in obj:
        try:
            if str(i.category.Name) in C.keys():
                C[str(i.category.Name)].append(i)
            else:
                C[str(i.category.Name)] = []
        except:
            C[str(i.category.Name)] = []
    D = {}
    for i in C:
        if (len(C[i]) == 0):
            pass
        else:
            D[i] = C[i]
    # print(D)
    return render(request, 'app/plans.html',{'obj':obj, 'categories': categories, 'C': D} )

# ****************************************************************
# Approve a subscription
# ****************************************************************
@login_required
def ApproveSubscription(request, user_id, plan_id,sub_id):
    try:
        p = plan.objects.get(user=User.objects.get(username=request.user.username), id = plan_id)
        s = subscription.objects.get(user = User.objects.get(id=user_id), id=sub_id, plan = p)
        s.approved = True
        s.save()
        messages.success(request, "Subscription has been approved succcessfully")
        # ****************************************************************
        # Email Settings
        # ****************************************************************
        subject = 'Subscription Alert'
        current_site = get_current_site(request)
        link_build = str(request.scheme) + "://" + str(current_site.domain) + str(reverse("Details", args=[plan_id,s.id ]))
        to_email = (s.user.email)
        content = f"A Subscription has been approved.Kindly visit the following link to see details.\n\t{link_build}"
        email = EmailMessage(subject, content, to=[to_email])
        email.send()
        return redirect("Plans")
    except Exception as e:
        print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    

# ****************************************************************
# Disapprove a subscription
# ****************************************************************
@login_required
def DisapproveSubscription(request, user_id, plan_id,sub_id):
    try:
        p = plan.objects.get(user=User.objects.get(username=request.user.username), id = plan_id)
        s = subscription.objects.get(user = User.objects.get(id=user_id), id=sub_id, plan = p)
        s.approved = False
        s.save()
        messages.success(request, "Subscription has been disapproved")
        # ****************************************************************
        # Email Settings
        # ****************************************************************
        subject = 'Subscription Alert'
        current_site = get_current_site(request)
        link_build = str(request.scheme) + "://" + str(current_site.domain) + str(reverse("Details", args=[plan_id,s.id ]))
        to_email = (s.user.email)
        content = f"A Subscription has been disapproved.Kindly visit the following link to see details.\n\t{link_build}"
        email = EmailMessage(subject, content, to=[to_email])
        email.send()
        return redirect("Plans")
    except Exception as e:
        # print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    
    
# ****************************************************************
# Edit a Subscription
# ****************************************************************
@login_required
def EditSubscription(request,plan_id,sub_id):
    try:
        p = plan.objects.get(id = plan_id)
        s = subscription.objects.get(
                    user=User.objects.get(
                        username=request.user.username
                    ),
                    plan = p
                )
        if request.method == "POST":
            p.number_of_open_slots = int(p.number_of_open_slots) + int(s.number_of_slots)
            p.save()
            s.number_of_slots = request.POST['number_of_slots']
            s.TotalAmount = int(p.currently_monthly_payment_per_line) * int(request.POST['number_of_slots'])
            s.save()
            # Reduced the plan available slots for subscription
            p.number_of_open_slots = int(p.number_of_open_slots) - int(s.number_of_slots)
            p.save()
            # ****************************************************************
            # Email Settings
            # ****************************************************************
            subject = 'Subscription Alert'
            current_site = get_current_site(request)
            link_build = str(request.scheme) + "://" + str(current_site.domain) + str(reverse("Details", args=[plan_id,s.id ]))
            to_email = (p.user.email)
            content = f"A Subscription has been modified.Kindly visit the following link to see details.\n\t{link_build}"
            email = EmailMessage(subject, content, to=[to_email])
            email.send()
            messages.success(request, "Account Owner has been notified about your subscription to this plan. Thanks")
            return redirect("dashboard")
        else:
            # print(s)
            template_name= "app/edit_subscription.html"
            slots =  int(s.number_of_slots) + int(p.number_of_open_slots)
            total = slots
            slots = [i for i in range(1, (slots) + 1)]
            context= {
                'slots' : slots,
                'plan': p,
                'subs':s,
                'total' : total
            }
            return render(request, template_name, context )
    
    except (plan.DoesNotExist, category.DoesNotExist) as e:
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    
    except Exception as e:
        messages.success(request, "Due to some technical reasons, subscription can not be edited right now. Sorry")
        return redirect("dashboard")

# ****************************************************************
# Subscription Detail View
# ****************************************************************
@login_required
def Detail(request, plan_id, sub_id):
    try:
        p = plan.objects.get(id = plan_id)
        s = subscription.objects.get(
                    user=User.objects.get(
                        username=request.user.username
                    ),
                    plan = p
                )
        template_name= "app/detail.html"
        context= {
            'plan': p,
            'subs':s,
        }
        return render(request, template_name, context )
    
    except (plan.DoesNotExist, category.DoesNotExist):
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    
    except Exception as e:
        # print(e)
        messages.success(request, "Due to some technical reasons, subscription can not be edited right now. Sorry")
        return redirect("dashboard")



# ****************************************************************
# Device Camptibility Handler View
# ****************************************************************
def deviceCompatibility(request):
    if request.method== "POST":
        messages.success(request, "Your request has been sent to your Account Owner.")
    template_name="app/device-campatibility.html"
    context = {
    
    }
    return render(request, template_name, context)
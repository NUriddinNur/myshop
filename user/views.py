from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create your views here.
from product.models import Category
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


def index(request):
    category = Category.objects.all()
    current_user = request.user

    profile = UserProfile.objects.get(user_id=current_user.id)
    context={
        'category': category,
        'profile': profile,
    }
    return render(request,'userprofile.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been update!')
            return HttpResponseRedirect('/user')
    category = Category.objects.all()
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    context = {
        'category': category,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your Password has been changed')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below!<br>', str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = ProfileUpdateForm(request.user)
        return render(request, 'user_password.html', {'form': form, 'category': category})


def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objrcts.filter(user_id=current_user.id)
    context = {
        'category': category,
        'current_user': current_user,
        'orders': orders
    }
    return render(request, 'user_orders.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage']=userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login error! User name or login incorrect!")
            return HttpResponseRedirect('/login')
        category = Category.objects.all()
        context = {'category': category,}
        return render(request, 'login_form.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Sizning akkauntingiz yaratildi!")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
        form = SignUpForm()
        category = Category.objects.all()
        context = {'category': category,
                   'form':form,
                   }
        return render(request, 'signup_form.html', context)





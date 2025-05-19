from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
# Message
from django.contrib import messages
 
# Authentication Form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate

# Forms & Model
from LoginApp.models import Profile
from LoginApp.forms import ProfileForm, SignUpForm

        # Registration
def signUpUser(request):
    if not request.user.is_authenticated:
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'Account create Successfully!')
                return HttpResponseRedirect(reverse('LoginApp:login'))
        return render(request, 'Login/signup.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('Shop:test'))

        # Login User
def loginUser(request):
    if not request.user.is_authenticated:
        form = AuthenticationForm()
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username') # username==>email
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request,user)
                    messages.info(request,'Login Successfully!')
                    return HttpResponseRedirect(reverse('LoginApp:profile'))
                    # return HttpResponse('Logged in')
        return render(request, 'Login/login.html',{'form':form})
    else:
        return HttpResponseRedirect(reverse('LoginApp:profile'))

        # User Profile
@login_required
def profile(request):
    userprofile = Profile.objects.get(user=request.user)
    return render(request,'Login/profile.html',{'userprofile':userprofile})

        # Update Profile
@login_required
def userProfile(request):
    profile = Profile.objects.get(user=request.user)

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            form = ProfileForm(instance=profile)
            messages.warning(request,'Profile update successfully!')
    return render(request, 'Login/change-profile.html',{'form':form})


        # Logout
@login_required
def logoutUser(request):
    logout(request)
    messages.warning(request,'Logout successfully!')
    return HttpResponseRedirect(reverse('Shop:home'))
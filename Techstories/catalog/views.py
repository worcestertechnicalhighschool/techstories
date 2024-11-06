from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect

def index(request):
    context = { }
    return render(request, 'index.html', context=context)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect(reverse('users-profile'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
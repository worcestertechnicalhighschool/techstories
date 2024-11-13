from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from .forms import UpdateUserForm, UpdateProfileForm, FollowForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def index(request): 


    following = Profile.objects.filter(followers = request.user.profile)
    posts = Post.objects.filter(author__in = following)

    return render(request, 'index.html', context={'posts': posts})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect(reverse('profile'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ProfileListView(generic.ListView):
    model = Profile

class PostDetailView(generic.DetailView):
    model = Post

@login_required
def profile_detail_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    followed = profile.followers.contains(request.user.profile)

    if request.method == 'POST':
        form = FollowForm(request.POST)
        if (form.is_valid()):
            if (form.cleaned_data.get("btn") == "Follow"):
                profile.followers.add(request.user.profile)
                followed = True
            if (form.cleaned_data.get("btn") == "Unfollow"):
                profile.followers.remove(request.user.profile)
                followed = False

    return render(request, 'catalog/profile_detail.html', context={'profile': profile, 'followed': followed })

class PostCreate(CreateView):
    model = Post
    fields = ['image', 'title', 'caption']
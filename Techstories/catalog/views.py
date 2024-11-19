from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from .forms import UpdateUserForm, UpdateProfileForm, FollowForm, LikeForm, UpdatePostForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from .forms import CreatePostForm
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

@login_required
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

@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = LikeForm(request.POST)
        if (form.is_valid()):
            if (form.cleaned_data.get("btn") == "Like"):
                post.likes.add(request.user.profile)
            if (form.cleaned_data.get("btn") == "Unlike"):
                post.likes.remove(request.user.profile)

    liked = post.likes.contains(request.user.profile)
    return render(request, 'catalog/post_detail.html', context= {'post': post, 'liked': liked, 'owned': post.author == request.user.profile})

@login_required
def profile_detail_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if (form.is_valid()):
            if (form.cleaned_data.get("btn") == "Follow"):
                profile.followers.add(request.user.profile)
            if (form.cleaned_data.get("btn") == "Unfollow"):
                profile.followers.remove(request.user.profile)

    followed = profile.followers.contains(request.user.profile)
    return render(request, 'catalog/profile_detail.html', context={'profile': profile, 'followed': followed})

@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        form.author = request.user.profile
        if form.is_valid():
            form.save()
        return render(request, 'catalog/post_form.html', context={'form': form })
    else:
        form = CreatePostForm()

    return render(request, 'catalog/post_form.html', context={'form': form })

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('profiles')

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("post-delete", kwargs={"pk": self.object.pk})
            )
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    context = {
        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm

# Create your views here.
""" @login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) """

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, "Your account has been created!"
                )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'webapp/register.html', {'form_register': form})

def login(request):
    pass

@login_required
def profile(request):
    #movies = request.user.customer.movies_set.all()
    #context = {'movies':movies}
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user )
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)

    context = {'update_form':update_form}
    
    return render(request, 'users/profile.html', context)

def favoritelist(request):
    return render(request, 'users/favoritelist.html')    

def userrate(request):
    return render(request, "users/userrate.html")

def userfavoritegrid(request):
    return render( request, "users/userfavoritegrid.html")
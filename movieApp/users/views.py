from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from web.forms import UserRegisterForm, UserUpdateForm

# Create your views here.
""" @login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) """
@login_required
def profile(request):
    #movies = request.user.customer.movies_set.all()
    #context = {'movies':movies}
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)

    context = {'update_form':update_form}
    
    return render(request, 'Users/userprofile.html', context)

def favoritelist(request):
    return render(request, 'Users/userfavoritelist.html')    
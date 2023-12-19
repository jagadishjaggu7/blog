from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def register(request):
    if request.method  == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Congrats your account has been created BOT!')
            return redirect('login')
    else:    

        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})
@login_required
def profile(request):
    if request.method  == 'POST':
        u_form = UserUpdateForm(request.POST,instance= request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, 
                                   instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Congrats your profile has been updated')
            return redirect('profile')
        else:
             messages.warning(request,f'sorry something went wrong')
             return redirect('profile')


    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)
        # messages.warning(request,f'sorry something went wrong')
        # return redirect('profile')

    context = {
        'u_form' : u_form,
        'p_form' : p_form

    }
    return render (request,'users/profile.html',context)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            try:
                # Attempt to get the user's profile
                profile = self.request.user.profile
            except ObjectDoesNotExist:
                # Redirect to register page if the profile doesn't exist
                messages.warning(self.request, 'You don\'t have an account. Please create an account to login.')
                return redirect('register')

        # Continue with the default behavior
        return super().form_valid(form)
    



    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, ShippingAddressForm, Account

# Create your views here.
def welcome_page(request):
    return render(request, "UsersAuthentication/welcome.html")

def signup_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signup')
    
    else:
        if request.method == 'POST':
            user_form = RegistrationForm(request.POST, request.FILES)
            shipping_address_form = ShippingAddressForm(request.POST)

            if user_form.is_valid() and shipping_address_form.is_valid():
                user = user_form.save()  # Save the user instance
                profile_picture = user_form.cleaned_data['profile_picture']
                profile = Account(user=user, profile_picture=profile_picture)
                profile.save()

                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.account = user
                shipping_address.save()
                return redirect('login')
            else:
                messages.error(request, 'Fill out the necessary informations.')
        else:
            user_form = RegistrationForm()
            shipping_address_form = ShippingAddressForm()

        return render(request, 'UsersAuthentication/signup.html', {'user_form': user_form, 'shipping_address_form': shipping_address_form})
    
def login_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home')
            
            else:
                messages.error(request, 'Invalid email or password.', extra_tags='login_error')

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return render(request, 'UsersAuthentication/login.html')
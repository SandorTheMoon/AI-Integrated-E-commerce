from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, ShippingAddressForm, Account, ProductForm
from .models import Product

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
    

# @login_required(login_url="/login/")
def logout_account(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    

# @login_required(login_url="/login/")
def home_page(request):
    products = Product.objects.all()
    return render(request, 'Home/Home.html', {'products': products })



# @login_required(login_url="/login/")
def addproduct_page(request):
    if request.method == 'POST':
        add_product_form = ProductForm(request.POST, request.FILES)

        if add_product_form.is_valid():
            print("product saved")
            add_product_form.instance.account = request.user
            add_product_form.save()
            return redirect('profile')
        else:
            print("product not saved due to invalid form")
    else:
        add_product_form = ProductForm()
        print("GET request, product form initialized")

    return render(request, 'Profile/addproduct.html', {'add_product_form': add_product_form})
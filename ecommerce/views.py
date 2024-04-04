from django.db.models import Q
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect, get_object_or_404

from order.admin import ContactUsAdmin
from order.models import ContactUs
from .forms import SignUpForm
from django.contrib.auth.models import User

from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from products.models import Product,Category
from django.contrib import messages
from .forms import UpdateUserForm




# Create your views here.

def Homepage(request):
    products = Product.objects.all()[0:10]
    return render(request, 'ecommerce/homepage.html', {'products': products})
def AboutUsPage(request):

    return render(request, 'ecommerce/aboutUs.html')





def contactUsView(request):
    return render(request, 'ecommerce/contactUs.html')
def meet_the_team(request):
    return render(request, 'meetTheTeam.html')

def privacy_Policy(request):
    return render(request, 'privacyPolicy.html')

def about_us(request):
    return render(request, 'ecommerce/aboutUs.html')

def ajax_contact_form(request):
    if request.method == 'POST':  # Ensure that this view is accessed via a POST request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create a ContactUs object and save it to the database
        contact_entry = ContactUs.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        # Return a JSON response indicating success
        data = {
            "bool": True,
            "message": "Your message has been successfully sent!"
        }
        return JsonResponse({"data": data})
    else:
        # Return a JSON response indicating that the request method is not allowed
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


def SignUp(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def Login(request):
    return render(request, 'registration/login.html')

@login_required
def My_account(request):
    return render(request, 'ecommerce/my_Account.html')



# TO BE FIXED TO BE FIXED TO BE FIXED TO BE FIXED
@login_required
def edit_my_account(request, pk):
    # Using get_object_or_404 to handle cases where user does not exist
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        try:
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.username = request.POST.get('username')
            user.save()

            messages.success(request, "User has been successfully updated")
            return redirect('/my_Account/')
        except IntegrityError:
            error_message = "Username already exists. Please choose a different username."

            return render(request, 'ecommerce/my_account_edit.html', {'user': user, 'error_message': error_message})

            # return redirect(f'/my_Account/my-account_edit/{pk}/')



    context = {
        'user': user  # using a meaningful key for the user object
    }
    return render(request, 'ecommerce/my_account_edit.html', context)
# @login_required
# def Edit_my_account(request):
    # if request.method == 'POST':
    #     user = request.user
    #     user.first_name = request.POST.get('first_name')
    #     user.last_name = request.POST.get('last_name')
    #     user.email = request.POST.get('email')
    #     user.username = request.POST.get('username')
    #     user.save()

#         # Retrieve the updated user object from the database
#         updated_user = User.objects.get(pk=user.pk)
#         print(updated_user)
#         return redirect('my_Account/')
#     return render(request, 'ecommerce/edit_my_Account.html')



@login_required
def Shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    active_category = request.GET.get('category', '')

    query = request.GET.get('query', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if active_category:
        products = products.filter(category__slug=active_category)

    context={
        'products': products,
        'categories': categories,
        'active_category': active_category,

    }
    return render(request, 'ecommerce/shop.html', context)

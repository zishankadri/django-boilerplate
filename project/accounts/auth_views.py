from django.shortcuts import render, HttpResponse, redirect

from accounts.models import UserAccount
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from accounts.models import UserAccount
from .forms import UserAccountForm

from .utils import generate_ref_code, send_email
from .emails import send_verification_email, send_change_password_email

def register_page(request):
    domain_name = request.build_absolute_uri('/')[:-1]

    if request.method == "POST":
        form = UserAccountForm(request.POST)

        if form.is_valid():
            user = form.save()
            send_verification_email(email=user.email, auth_token=user.email_auth_token, domain_name=domain_name)
            messages.success(request, "Registration successful!")
            
            return render(request, "accounts/check_your_email.html", {'email': user.email})
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
                    
            return render(request, "accounts/register.html", { 'form': form })
                
    user_form = UserAccountForm()

    context = {
        'form': user_form,
    }

    return render(request, "accounts/register.html", context)


def login_page(request):
    # user = request.user
    domain_name = request.build_absolute_uri('/')[:-1]
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.verified_email:
                # Send verification codes again
                send_verification_email(email=user.email, auth_token=user.email_auth_token, domain_name=domain_name)
                messages.info(request, f'This Accounts email is not verified')
                return render(request, "accounts/check_your_email.html", {'email': user.email})

            login(request, user)
            return redirect("/classes/")

        else:
            messages.error(request, f'The email or password is incorrect')

    return render(request, "accounts/login.html")


def logout_page(reqeust):
    logout(reqeust)
    return redirect("/")


def verify_email_page(request, auth_token):
    try:
        user = UserAccount.objects.get(email_auth_token=auth_token)

        user.verified_email = True
        user.save()

        messages.success(request, f'Your email has been verified!')
        return redirect("/accounts/login/")

    except:
        return redirect("/accounts/error/")


def forgot_password(request):
    domain_name = request.build_absolute_uri('/')[:-1]

    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = UserAccount.objects.get(email=email)
        except:
            messages.info(request, f'Incorrect email.')
            return render(request, "accounts/login.html")
        
        send_change_password_email(email=user.email, auth_token=user.email_auth_token, domain_name=domain_name)
        print("success")
        return render(request, "accounts/check_your_email.html", {'email': user.email})

    return render(request, "accounts/forgot_password.html")

# @login_required
def change_password(request, email, auth_token):
    try:
        user = UserAccount.objects.get(email=email)
        if not user.verified_email:
            messages.info(
                request, f'This email is not verified, register again to get verification emial.')
            return redirect("/accounts/register/")
    except:
        messages.info(request, f'Incorrect email.')
        return render(request, "accounts/login.html")

    if user.email_auth_token != auth_token:
        return redirect("accounts/error/")

    if request.method == "POST":
        new_password = request.POST["new_password"]
        conform_new_password = request.POST["confirm_password"]

        # Gate keeping.
        if new_password != conform_new_password:
            messages.error(
                request, "Passwords didn't match, Please try again.")
            return redirect(f"/accounts/change_password/{user.email}/{user.email_auth_token}/")
        if len(new_password) < 8:
            messages.error(
                request, "Passwords must contain at least 8 characters.")
            return redirect(f"/accounts/change_password/{user.email}/{user.email_auth_token}/")

        # All Correct.

        # Record change in history.
        subject = "Changed Password"
        previous_value = str(user.password)
        latest_value = new_password
        # user.record_history(subject, previous_value, latest_value)

        # OK, Change password.
        user.set_password(new_password)
        user.auth_token = generate_ref_code()
        user.save()

        messages.success(request, "Password changed successfully!")
        return redirect('/')

    return render(request, "accounts/change_password.html")







# Trash

@login_required
def profile_page(request):
    domain_name = request.build_absolute_uri('/')[:-1]

    user = request.user
    if user.is_anonymous:
        return redirect("/register/")

    if request.method == "POST":

        # user.auth_token = generate_auth_token()
        if "change_password" in request.POST:
            user.auth_token = generate_ref_code()
            user.save()

            subject = "Change Password"
            message = f'''
                    Change password for Algostockz by clicking :- 
                    {domain_name}/accounts/change_password/{user.email}/{user.auth_token}/
                    '''
            send_email(subject=subject, message=message, email=user.email)

            return render(request, "accounts/check_your_email.html", context={"email": request.user.email})

        if "change_email" in request.POST:
            user.auth_token = generate_ref_code()
            user.save()

            subject = "Change Email"
            message = f"Change Email for Algostockz by clicking :- {domain_name}/accounts/change_email/{user.auth_token}/"
            send_email(subject=subject, message=message, email=user.email)

            return render(request, "accounts/check_your_email.html", context={"email": request.user.email})

        if "change_phone" in request.POST:
            # Verify current email here.
            user.auth_token = generate_ref_code()
            user.save()

            return redirect(f"/change_phone/{user.auth_token}/")

        if "logout" in request.POST:
            return redirect("/logout/")

    context = {
        'email': user.email,
        'phone': user.phone,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def change_email_page(request, auth_token):
    user = request.user
    domain_name = request.build_absolute_uri('/')[:-1]

    if user.auth_token != auth_token:
        return redirect("/accounts/error/")

    if request.method == "POST":
        new_email = request.POST["new_email"]
        conform_new_email = request.POST["conform_new_email"]

        # Gate keeping.
        if new_email != conform_new_email:
            messages.error(request, "Emails didn't match, Please try again.")
            return redirect(f"/accounts/change_email/{user.auth_token}/")

        try:
            user = UserAccount.objects.get(email=new_email)
            messages.error(request, "Email already exist.")
            return redirect(f"/accounts/change_email/{user.auth_token}/")
        except:
            pass

        if len(new_email) <= 4:
            messages.error(request, "Emails didn't match, Please try again.")
            return redirect(f"/accounts/change_email/{user.auth_token}/")

        # All Correct.

        # OK, Change password.
        user.changing_email = new_email
        user.auth_token = generate_ref_code()
        user.save()

        subject = "Verify your email address"
        message = f"Verify your email for Algostockz by clicking :- {domain_name}/accounts/change_email_final/{user.auth_token}/"
        send_email(subject=subject, message=message, email=new_email)

        return render(request, "accounts/check_your_email.html", context={"email": new_email})

    return render(request, "accounts/change_email.html")


def change_email_verified(request, auth_token):
    try:

        user = UserAccount.objects.get(auth_token=auth_token)

        # Record change in history.
        subject = "Changed Email"
        previous_value = user.email
        latest_value = user.changing_email
        user.record_history(subject, previous_value, latest_value)

        user.email = user.changing_email
        user.auth_token = generate_ref_code()
        user.save()

        messages.success(request, "Email changed successfully!")
        return redirect("/accounts/profile/")

    except:
        return redirect("/accounts/error/")

def check_your_email(request):
    return render(request, "accounts/check_your_email.html", context={"email":request.user.email})

def error(request):
    return render(request, "accounts/error.html")


@login_required
def change_phone_page(request, auth_token):
    user = request.user
    try:
        if not user.is_verified:
            messages.info(
                request, f'This email is not verified, register again to get verification emial.')
            return redirect("/accounts/register/")
    except:
        messages.info(request, f'Incorrect email.')
        return render(request, "accounts/login.html")

    if user.auth_token != auth_token:
        return redirect("accounts/error/")

    if request.method == "POST":
        new_phone = request.POST["new_phone"]

        subject = "Changed Phone Number"
        previous_value = str(user.phone)
        latest_value = str(new_phone)
        user.record_history(subject, previous_value, latest_value)

        # OK, Change phone.
        user.phone = new_phone
        user.auth_token = generate_ref_code()
        user.save()

        messages.success(request, "Phone changed successfully!")
        return redirect(f"/")

    return render(request, "accounts/change_phone.html")



def verify_phone_page(request, auth_token):
    try:
        user = UserAccount.objects.get(phone_auth_token=auth_token)

        user.verified_phone = True
        user.save()

        messages.success(request, f'Your phone number has been verified!')
        return redirect("/accounts/login/")

    except:
        return redirect("/accounts/error/")












# Sign-in & Log-in Client
# def register_page(request):
#     domain_name = request.build_absolute_uri('/')[:-1]

#     if request.method == "POST":
#         cuit = request.POST['cuit']
#         password = request.POST['password']
#         phone = request.POST['phone']
#         full_name = request.POST['full_name']
#         user_type = request.POST['user_type']

#         # If this email already exist.
#         if UserAccount.objects.filter(cuit=cuit).exists():
#             messages.info(request, "This Email already exist go to log-in page")
#             return redirect("/accounts/login/")

#         # Password criteria {
#         if len(password) < 8:
#             messages.error(request, "Passwords must contain at least 8 characters.")
#             return redirect(f"/accounts/register/")
#         if len(str(phone)) > 14 or len(str(phone)) < 10:
#             messages.error(request, "Length of the phone number must be between 10 and 14.")
#             return redirect(f"/accounts/register/")
#         try:
#             int(phone)
#         except:
#             messages.error(request, "Invalid phone number, please try again.")
#             return redirect(f"/accounts/register/")
#         # }

#         # Create an un-verified UserAccount
#         # user = UserAccount.objects.create_user(email=email, password=password, phone=phone)
#         user = UserAccount.objects.create_user(cuit=cuit, password=password, phone=phone)
#         user.full_name = full_name
#         user.user_type = user_type
#         user.save()

#         messages.success(request, "success!")

#         # return render(request, "check_your_email.html", context={"email":email})
#         return redirect('/')

#     user_account_form = UserAccountForm()
#     carrier_specific_form =  CarrierSpecificsForm()

#     context = {
#         'user_form': user_account_form,
#         'carrier_specific_form': carrier_specific_form,
#     }

#     return render(request, "accounts/register.html", context)



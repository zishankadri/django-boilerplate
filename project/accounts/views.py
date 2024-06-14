from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# My Profile View (Edit)
# @login_required
# def my_profile(request):
#     user = request.user

#     if request.method == "POST":
#         user.profile.update(request)

#     context = {
#         'user': user,
#     }
#     return render(request, "my_profile.html", context)

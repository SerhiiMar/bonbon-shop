from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import LoginForm, RegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect("catalog:product_list")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print("is valid")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.error(request, "Invalid login or password")

                return redirect("accounts:login")

            login(request, user)
            print(request.session.get("cart"))
            # request.session["cart"]
            return redirect("catalog:product_list")
        else:
            print("not valid")
            return render(request, "accounts/login.html", {"form": form})

    form = LoginForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("catalog:product_list")


class UserCreateView(generic.CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

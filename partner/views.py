from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PartnerForm


# Create your views here.
def index(request):
    ctx = {}
    if request.method == "GET":
        partner_form = PartnerForm()
        ctx.update({"form": partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(request.POST)
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"form": partner_form})
    return render(request, "index.html", ctx)

    # ctx = {}
    # return render(request, "index.html", ctx)


def login(request):
    ctx = {}
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            return redirect("/partner/")
        else:
            # Return an 'invalid login' error message.
            ctx.update({"error": "사용자가 없습니다. "})

    return render(request, "login.html", ctx)


def signup(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 유저생성
        user = User.objects.create_user(username, email, password)

        # 장고 User 메서드를 상용하지 않을 경우 아래와 같이 유저 생성
        # Article.object.create(title="", content="")

        # print(username, email, password)
    ctx = {}
    return render(request, "signup.html", ctx)


def logout(request):
    auth_logout(request)
    return redirect("/partner/")

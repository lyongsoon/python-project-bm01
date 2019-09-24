from django.contrib.auth import (
    authenticate,
    login as auth_login,
)
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

# from src.partner.models import Partner

# from src.partner.models import Partner
from partner.models import Partner
from .models import Client


def index(request):
    partner_list = Partner.objects.all()
    ctx = {
        "partner_list": partner_list
    }
    return render(request, "main.html", ctx)


def common_login(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print('user', username)
        user = authenticate(username=username, password=password)
        # print('user', user)
        if user is not None:
            # print('user', user)
            # print('group', group)
            if group not in [group.name for group in user.groups.all()]:
                # if group not in user.groups.all():
                ctx.update({"error": "접근권한이 없습니다. "})

                # 콘솔 기반 디버깅 방법
                # for group in user.groups.all():
                #     print("group:", group)
            else:
                auth_login(request, user)
                # URL 뒤에 파라미터가 있는지 확인
                next_value = request.GET.get("next")
                if next_value:
                    return redirect(next_value)
                else:
                    if group == "partner":
                        return redirect("/partner/")
                    else:
                        return redirect("/")
        else:
            # Return an 'invalid login' error message.
            ctx.update({"error": "사용자가 없습니다. "})

    return render(request, "login.html", ctx)


def login(request):
    ctx = {"is_client": True}
    return common_login(request, ctx, "client")


def common_signup(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 유저생성
        user = User.objects.create_user(username, email, password)
        target_group = Group.objects.get(name=group)
        user.groups.add(target_group)

        if group == "client":
            Client.objects.create(user=user, name=username)
        # else:
        #     # rollback 로직 추가 필요
        #     pass

        # 장고 User 메서드를 상용하지 않을 경우 아래와 같이 유저 생성
        # Article.object.create(title="", content="")

        # print(username, email, password)
    return render(request, "signup.html", ctx)


def signup(request):
    ctx = {"is_client": True}
    return common_signup(request, ctx, "client")

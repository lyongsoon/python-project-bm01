from django.contrib.auth import (
    authenticate,
    login as auth_login,
)
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

# from src.partner.models import Partner
from partner.models import Partner, Menu
from client.models import Client, Order, OrderItem


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


def order(request, partner_id):
    ctx = {}

    partner = Partner.objects.get(id=partner_id)
    menu_list = Menu.objects.filter(partner=partner)
    if request.method == "GET":
        ctx.update({
            "partner": partner,
            "menu_list": menu_list,
        })
    elif request.method == "POST":

        # # CASE2
        order = Order.objects.create(
            Client=request.user.client,
            address="test",
        )
        for menu in menu_list:
            menu_count = request.POST.get(str(menu.id))
            menu_count = int(menu_count)
            if menu_count > 0:
                item = OrderItem.objects.create(
                    order=order,
                    menu=menu,
                    count=menu_count
                )
                # order.items.add(item)

        return redirect("/")

        # # CASE1
        # menu_dict = {}
        # for menu in menu_list:
        #     # menu.id 를 String 으로 Casting
        #     # menu_count = request.POST.get("{}".format(menu.id))
        #     menu_count = request.POST.get(str(menu.id))
        #     if int(menu_count) > 0:
        #         menu_dict.update({str(menu.id): menu_count})
    return render(request, "order_menu_list.html", ctx)

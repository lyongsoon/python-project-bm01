from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect


# from src.client.views import common_login, common_signup
from client.views import common_login, common_signup
from .models import Menu
from .forms import PartnerForm, MenuForm

URL_LOGIN = '/partner/login'


def partner_group_check(user):
    return "partner" in user.groups.all()


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
    return common_login(request, ctx, "partner")


def signup(request):
    ctx = {}
    return common_signup(request, ctx, "partner")


def logout(request):
    auth_logout(request)
    return redirect("/partner/")


@login_required(login_url=URL_LOGIN)
def edit_info(request):
    ctx = {}
    # Article.objects.all() % query
    # partner = Partner.objects.get(user=request.user)
    # partner_form = PartnerForm(instance=request.user.partner)
    # ctx.update({"form": partner_form})

    if request.method == "GET":
        partner_form = PartnerForm(instance=request.user.partner)
        ctx.update({"form": partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(
            request.POST,
            instance=request.user.partner
        )
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"form": partner_form})
    return render(request, "edit_info.html", ctx)


# Case 1 : 파트너 오브젝트가 없을 경우 즉 로그인 하지 않고 접근하려고 할 경우
@login_required(login_url=URL_LOGIN)
def menu(request):
    ctx = {}

    # Case 2 : 파트너 오브젝트가 없을 경우 즉 로그인 하지 않고 접근하려고 할 경우
    # if request.user.is_anonymous or request.user.partner is None:
    #     return redirect("/partner")
    menu_list = Menu.objects.filter(partner=request.user.partner)
    ctx.update({"menu_list": menu_list})
    return render(request, "menu_list.html", ctx)


@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_add(request):
    ctx = {}

    # # partner 객체가 유저그룹에 있느지 체크, 없을 경우 홈 페이지로 이동
    # if "partner" not in request.user.groups.all():
    #     return redirect("/")

    if request.method == "GET":
        form = MenuForm()
        ctx.update({"form": form})
    elif request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            lv_menu = form.save(commit=False)
            lv_menu.partner = request.user.partner
            lv_menu.save()
            return redirect("/partner/menu")
        else:
            ctx.update({"form": form})

    return render(request, "menu_add.html", ctx)


@login_required(login_url=URL_LOGIN)
def menu_detail(request, menu_id):
    lv_menu = Menu.objects.get(id=menu_id)
    ctx = {"menu": lv_menu}
    return render(request, "menu_detail.html", ctx)


@login_required(login_url=URL_LOGIN)
def menu_edit(request, menu_id):
    ctx = {"replacement": "수정"}
    lv_menu = Menu.objects.get(id=menu_id)

    if request.method == "GET":
        form = MenuForm(instance=lv_menu)
        ctx.update({"form": form})
    elif request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=lv_menu)
        if form.is_valid():
            lv_menu = form.save(commit=False)
            lv_menu.partner = request.user.partner
            lv_menu.save()
            return redirect("/partner/menu")
        else:
            ctx.update({"form": form})

    return render(request, "menu_add.html", ctx)


@login_required(login_url=URL_LOGIN)
def menu_delete(request, menu_id):
    lv_menu = Menu.objects.get(id=menu_id)
    lv_menu.delete()
    return redirect("/partner/menu")

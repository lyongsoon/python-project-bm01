from django.urls import path
# from django.conf.urls import url
from .views import (
    signup,
    edit_info,
    index, login, logout,
    menu, menu_add,
)

urlpatterns = [
    # path('partner/', include('partner.urls')),
    # path('partner/', include('partner.urls')),
    path('', index, name="index"),
    path('signup', signup, name="signup"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('edit', edit_info, name="edit"),
    path('menu', menu, name="menu"),
    path('menu/add', menu_add, name="menu_add"),
    # url(r'^$', signup, name="signup"),
]
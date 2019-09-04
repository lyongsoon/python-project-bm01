from django.urls import path, include
# from django.conf.urls import url
from .views import signup, index, login, logout

urlpatterns = [
    # path('partner/', include('partner.urls')),
    # path('partner/', include('partner.urls')),
    path('', index, name="index"),
    path('signup', signup, name="signup"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    # url(r'^$', signup, name="signup"),
]
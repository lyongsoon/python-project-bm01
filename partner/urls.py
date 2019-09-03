from django.urls import path, include
# from django.conf.urls import url
from .views import signup

urlpatterns = [
    # path('partner/', include('partner.urls')),
    # path('partner/', include('partner.urls')),
    path('', signup, name="signup"),
    # url(r'^$', signup, name="signup"),
]
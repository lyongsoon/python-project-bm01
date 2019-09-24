from django.urls import path
from .views import (
    index, signup, login, order,
)

urlpatterns = [
    path('', index, name="index"),
    path('signup', signup, name="signup"),
    path('login', login, name="login"),
    path('<int:partner_id>/', order, name="order"),
]

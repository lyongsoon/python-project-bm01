from django.db import models
from django.contrib.auth.models import User
# from src.partner.models import Menu
from partner.models import Menu


# Create your models here.
class Client(models.Model):
    # User 와의 관계 지정
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50,
        verbose_name="고객 이름",  # 한글 레이블 출력
    )


class Order(models.Model):
    Client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(
        max_length=100,
        verbose_name="주소",  # 한글 레이블 출력
    )
    created_at = models.DateTimeField(auto_now_add=True)

    items = models.ManyToManyField(
        Menu,
        through='OrderItem',    # OrderItem 클라스는 본 클라스 생성 후 생성되는 크라스라서 스트링으로 표시
        through_fields=('order', 'menu'),
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()

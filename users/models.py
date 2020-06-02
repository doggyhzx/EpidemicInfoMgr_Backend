from django.contrib.auth.models import AbstractUser
from django.db import models


# 自定义的用户类
class UserInfo(AbstractUser):
    userRole = (
        ('v', 'visitor'),
        ('n', 'normal'),
        ('sa', 'super-admin'),
        ('a1', 'admin-1'),
        ('a2', 'admin-2'),
        ('a3', 'admin-3'),
        ('a4', 'admin-4'),
    )
    # 用户uid 用户对象的唯一标识符
    # 用于显示的用户名
    # 用户的电子邮箱，用于邮箱验证
    # 密码
    # 使用基类中的属性

    # 用户的真实姓名
    real_name = models.CharField(max_length=25)

    # 用户的电话号码
    phone = models.CharField(max_length=11)
    # 用户的角色分组，决定了用户的行为权限
    role = models.CharField(max_length=20, choices=userRole)
    # 用户的身份证号
    citizen_id = models.CharField(max_length=18)

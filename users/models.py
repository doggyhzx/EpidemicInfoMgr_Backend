from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from EpidemicInfoMgr_Backend import settings


# 自定义的用户管理类
class MyUserManager(BaseUserManager):
    def _create_user(self, username, password, phone, email, real_name, citizen_id, **kwargs):
        if not phone:
            raise ValueError('必须要传递手机号')
        if not password:
            raise ValueError('必须要输入密码')
        if not username:
            raise ValueError('必须要传递用户名')
        if not email:
            raise ValueError('必须要输入邮箱')
        if not real_name:
            raise ValueError('必须要传递真实姓名')
        if not citizen_id:
            raise ValueError('必须要输入身份证号')
        user = self.model(username = username, password = password, phone = phone, email = email, real_name = real_name, citizen_id = citizen_id, **kwargs)
        user.set_password(password)
        user.save()
        return user

    # 创建普通用户
    def create_user(self, username, password, phone, email, real_name, citizen_id, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, phone, email, real_name, citizen_id, **kwargs)

    # 创建超级用户
    def create_superuser(self, username, password, phone, email, real_name, citizen_id, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, settings.DEFAULT_SUPERUSER_INFO["phone"], email, settings.DEFAULT_SUPERUSER_INFO["real_name"], settings.DEFAULT_SUPERUSER_INFO["citizen_id"], **kwargs)


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

    objects = MyUserManager()

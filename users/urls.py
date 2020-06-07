"""EpidemicInfoMgr_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # GET:进到个人主页，返回用户的JSON数据
    path('profile/', views.OnGotoUserProfile),
    # POST:用户提交修改信息 JSON字段：username phone email citizen_id real_name 里面的一个或多个
    path('profile/modify/', views.OnModifyProfilePosted),
    # GET: 发送验证邮件
    path('profile/changepass/', views.OnChangePasswordRequest),
    # 这个URL后面会带一个token， 不管GET还是POST都会验证TOKEN合法性
    # GET: 跳转到修改密码的页面 POST：在邮箱验证成功以后的页面，点击确认修改，修改用户的密码并登出 字段：new_password
    path('profile/changepass/set_new/', views.OnConfirmNewPassword),
    # GET：跳转到登录
    path('login/', views.OnGotoLoginPage),
    # POST: 提交登录信息 JSON 字段：username password
    path('login/post/', views.OnLoginRequest),
    # GET：转向注册页面
    path('register/', views.OnGotoRegisterPage),
    # POST：注册页面 JSON 字段：username password phone email citizen_id real_name
    path('register/post/', views.OnRegisterFormSubmit),
    # GET:登出
    path('logout/', views.OnLogoutRequest),
    # GET: 注册的邮箱验证确认
    path('mail/confirm/reg/', views.OnRegisterMailConfirmed),
    # GET: 点击邮件里的验证链接 跳转到修改密码的页面
    path('mail/confirm/changepass/', views.OnChangePassMailConfirmed),
    # POST： 超级管理员给其他用户授权 JSON 字段 targetUser targetGroup
    path('auth/authorization/', views.OnUserAuthorizationRequest),
    # GET: 无权访问的时候 转到无权访问页面
    path('auth/forbidden/', views.OnPermissionDenied),
    path('createSuperUser', views.CreateSuperUser)

]

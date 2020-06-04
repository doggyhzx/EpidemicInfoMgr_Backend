from django.http import HttpResponse
from django.http import HttpRequest, JsonResponse
from django.contrib import auth
from django.core.mail import send_mail, send_mass_mail
from django import forms
from EpidemicInfoMgr_Backend import settings
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from . import models
from .decorators import group_required


# 表单的验证类
class UserInfoCheck(forms.Form):
    # 变量名字必须要跟form表单里的名字一一对应
    username = forms.CharField(error_messages={'required': '用户不能为空'})  # CharField表示传入的得是字符串
    password = forms.CharField(
        max_length=12,  # 最大字符串为12个
        min_length=6,  # 最小字符串为6个
        error_messages={'required': '密码不能为空', 'min_length': '最小字符为6个', 'max_length': '最大字符为12个'}
    )  # CharField表示传入的得是字符串
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱地址不正确'})  # EmailField表示传入的得是邮箱格式
    real_name = forms.CharField(error_messages={'required': '真实姓名不能为空'})
    phone = forms.RegexField(r"^1[3-9]\d{9}$", error_messages={'invalid': '手机号格式有误'})
    citizen_id = forms.RegexField(r"^[1-9][0-9]{5}([1][9][0-9]{2}|[2][0][0|1][0-9])([0][1-9]|[1][0|1|2])([0][1-9]|["
                                  r"1|2][0-9]|[3][0|1])[0-9]{3}([0-9]|[X])$", error_messages={'invalid': '身份证号格式有误'})


# 下面是各个视图函数
# 访问首页时
def OnRequestHome(request: HttpRequest):
    return JsonResponse({"response": "请求主页成功！"})


# 点击注册按钮时 跳转到注册页面
def OnGotoRegisterPage(request: HttpRequest):
    return HttpResponse()


# 前端的注册表单提交时
def OnRegisterFormSubmit(request: HttpRequest):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    realName = request.POST['real_name']
    phoneNum = request.POST['phone']
    citizenID = request.POST['citizen_id']

    checkObj = UserInfoCheck(request.POST)
    checkRes = checkObj.is_valid()

    print(checkRes)

    if checkRes:
        # 验证通过之后返回正确信息的一个字典obj.cleaned_data，这是个字典
        # 此处如果是注册功能的话，就可以把注册信息的字典写入数据库
        print(checkObj.cleaned_data)
        try:
            user = models.UserInfo.objects.create_user(username, password, phoneNum, email, realName, citizenID)
            user.is_active = False
            user.save()
        except Exception as e:
            return HttpResponse("创建用户失败 %s" % (str(e)))

        AuthorizeUser(user, "common")
        user.save()

        try:
            SendAuthenticationMail(address=email, mode="register")
        except Exception as e:
            return HttpResponse("在发送验证邮件时出现问题 %s ，请点击页面上的按钮重新尝试发送" % (str(e)))

        return HttpResponse("注册成功！我们已经向您的邮箱地址发送了一封验证邮件，请点击其中的验证链接以激活您的账号")
    else:
        # 验证不通过之后返回一个所有的错误信息：obj.errors，是一大串字符串一个包含user、pwd、email错误信息的html格式的ul标签
        print(checkObj.errors)
        # 获取user的第一个错误信息
        # print(obj.errors['user'][0])
        return HttpResponse("注册失败，您提供的信息不合法，请检查后重新提交")

    #


# 邮箱验证的链接被点击时
def OnMailConfirmed(request: HttpRequest):
    return HttpResponse()


# 点击登录时 跳转到登录页面
def OnGotoLoginPage(request: HttpRequest):
    return HttpResponse()


# 点击登录按钮时，处理登录表单
def OnLoginRequest(request: HttpRequest):
    if Authenticate(request):
        auth.login(request, request.user)
        return HttpResponse("登录成功!")
    else:
        return HttpResponse("登录失败，用户名或密码有误")


# 超级管理员试图为某个账号授权时
@login_required
@group_required('superAdmin')
def OnUserAuthorizationRequest(request: HttpRequest):
    targetUserName = request.POST['targetUser']
    groupName = request.POST['targetGroup']
    targetUser = models.UserInfo.objects.filter()
    if groupName is not "common" or "admin-1" or "admin-2" or "admin-3" or "admin-4":
        return HttpResponse("目标用户组不存在")
    AuthorizeUser(targetUser, groupName)
    return HttpResponse("成功将用户%s 增加%s 分组" % (targetUserName, groupName))


# 为用户授权
def AuthorizeUser(user: models.UserInfo, group_name):
    group = Group.objects.get(name=group_name)
    if group:
        pass
    else:
        group = Group.objects.create(name=group_name)

    user.groups.add(group)
    return


# 请求进入到用户主页
@login_required
def OnGotoUserProfile(request: HttpRequest):
    return HttpResponse()


# 修改个人信息的提交
@login_required
def OnModifyProfilePosted(request: HttpRequest):
    keys = request.POST.keys()
    user = request.user

    return HttpResponse("信息修改成功")


# 鉴权函数
def Authenticate(request: HttpRequest):
    auth.authenticate(request, )
    return


# 发送验证邮件
def SendAuthenticationMail(address, mode):
    title, msg = "", ""
    if mode is "register":
        title = "注册验证----疫情防控系统邮箱验证"
        msg = "您收到该邮件是因为您已成功注册了疫情防控系统的用户，请点击下面的链接来激活您的账号，激活后您就可以通过账号登录到疫情防控系统中\n若非您本人操作，请忽略本条"
    elif mode is "changePassword":
        title = "密码修改验证----疫情防控系统邮箱验证"
        msg = "您正在请求修改密码，请点击下面的链接来完成身份确认，若非您本人操作，请忽略本条"
    else:
        return

    receiver = [
        address
    ]
    # 发送邮件
    send_mail(subject=title, message=msg, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=receiver)


# 点击修改密码 发送邮件
@login_required
def OnChangePasswordRequest(request: HttpRequest):
    try:
        SendAuthenticationMail(request, 'changePassword')
        return HttpResponse("我们已经向您发送了一封验证邮件，请点击其中的链接来重置您的密码")
    except Exception as e:
        return HttpResponse("邮件发送出错 %s，请重试" % (str(e)))


# 点了确认修改 实际去保存新的密码 并让用户重新登录
def OnConfirmNewPassword(request: HttpRequest):
    newPassword = request.POST['new_password']
    user = request.user
    user.set_password(newPassword)
    user.save()
    OnLogoutRequest(request)
    return HttpResponse("密码修改成功，请用新密码重新登录")


# 登出
@login_required
def OnLogoutRequest(request: HttpRequest):
    auth.logout(request)
    return HttpResponse("登出成功")


def OnTest(request: HttpRequest):
    return JsonResponse({"aa": "???????????"})


def CreateSuperUser(request: HttpRequest):
    return HttpResponse(request.headers.items)

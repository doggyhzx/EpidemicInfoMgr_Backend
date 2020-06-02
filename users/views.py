from django.http import HttpResponse
from django.http import HttpRequest,JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# 访问首页时
def OnRequestHome(request: HttpRequest):
    return HttpResponse()


# 点击注册按钮时 跳转到注册页面
def OnGotoRegisterPage(request: HttpRequest):
    return HttpResponse()


# 前端的注册表单提交时
def OnRegisterFormSubmit(request: HttpRequest):
    return HttpResponse()


# 邮箱验证的链接被点击时
def OnMailConfirmed(request: HttpRequest):
    return HttpResponse()


# 点击登录时 跳转到登录页面
def OnGotoLoginPage(request: HttpRequest):
    return HttpResponse()


# 点击登录按钮时，处理登录表单
def OnLoginRequest(request: HttpRequest):
    return HttpResponse()


# 超级管理员试图为某个账号授权时
def OnUserAuthorizationRequest(request: HttpRequest):
    return HttpResponse()


# 为用户授权
def AuthorizeUser(user):
    return


# 请求进入到用户主页
def OnGotoUserProfile(request: HttpRequest):
    return HttpResponse()


# 修改个人信息的提交
def OnModifyProfilePosted(request: HttpRequest):
    return HttpResponse()


# 鉴权函数
def Authenticate(request:HttpRequest):
    return 0


# 发送验证邮件
def SendAuthenticationMail(request: HttpRequest):
    return


# 输了确认密码以后，点击确认修改密码

def OnChangePasswordRequest(request: HttpRequest):
    if Authenticate(request) is not None:
        SendAuthenticationMail(request)
    else:
        pass
    return


# 登出
def OnLogoutRequest(request: HttpRequest):
    auth.logout(request)

def OnTest(request: HttpRequest):
    return JsonResponse({"aa": "???????????"})

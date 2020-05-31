from django.http import HttpResponse

#访问首页时
def OnRequestHomt(request):
    return HttpResponse()

#点击注册按钮时 跳转到注册页面
def OnGotoRegisterPage(request):
    return HttpResponse()

#前端的注册表单提交时
def OnRegisterFormSubmit(request):
    return HttpResponse()

#邮箱验证的链接被点击时
def OnMailConfirmed(request):
    return HttpResponse()

#点击登录时 跳转到登录页面
def OnGotoLoginPage(request):
    return HttpResponse()

#点击登录按钮时，处理登录表单
def OnLoginRequest(request):
    return HttpResponse()

#试图为某个账号授权时
def OnUserAuthorizationRequest(request):
    return HttpResponse()

#请求进入到用户主页
def OnGotoUserProfile(request):
    return HttpResponse()

#修改个人信息的提交
def OnModifyProfilePosted(request):
    return HttpResponse()

#鉴权函数
def Authenticate(needRole):
    return 0

#发送验证邮件
def SendAuthenticationMail(request):
    return

#输了确认密码以后，点击确认修改密码
def OnChangePasswordRequest(request):
    return

#登出
def OnLogoutRequest(request):
    return










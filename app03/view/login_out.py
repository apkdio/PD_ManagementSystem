from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect

from app03.middle_things.img_code import code_img
from app03.middle_things.password import md5
from app03.models import SuperManager, Department, Logging
from app03.view.forms import manager
from example01.settings import INITIAL_SETTING

user = INITIAL_SETTING['user']
depart_id = INITIAL_SETTING['depart_id']
depart_name = INITIAL_SETTING['depart_name']
password = INITIAL_SETTING['password']


def check_admin():
    # 初始化系统条件
    if not SuperManager.objects.filter(name=user).exists():
        Department.objects.create(id=depart_id, title=depart_name)
        SuperManager.objects.create(name=user, password=md5(password), depart_id=depart_id)


def login(request):
    check_admin()
    ses = request.session["info"]["name"]
    if ses and SuperManager.objects.filter(name=ses).exists():
        return redirect("/depart/list/")
    if request.method == 'GET':
        form = manager()
        return render(request, 'login.html', {"form": form})
    form = manager(data=request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {"form": form})
    code = form.cleaned_data.pop('code')
    form.cleaned_data["password"] = md5(form.cleaned_data['password'])
    user = SuperManager.objects.filter(**form.cleaned_data).first()
    if code.upper() != request.session.get("img_code", " ").upper():
        form.add_error("code", "验证码错误!")
        return render(request, 'login.html', {"form": form})
    if user is not None:
        request.session["info"] = {"id": user.id, "name": user.name, "depart": user.depart_id}
        Logging.objects.create(operate_user=user.name, action="Login", operate_object="Success")
        # 设置session超时24h
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/depart/list/')
    form.add_error("password", "用户名或者密码错误!")  # 主动增加错误信息
    Logging.objects.create(operate_user=form.cleaned_data["name"], action="Login", operate_object="Error")
    return render(request, 'login.html', {"form": form})


def logout(request):
    Logging.objects.create(operate_user=request.session["info"]["name"],
                           action="Logout", operate_object="Success")
    request.session.flush()
    return redirect("/main")


def image_code(request):
    img, string = code_img()
    stream = BytesIO()
    img.save(stream, 'png')
    # 将字符写入session,写入内存,不存 到项目中
    request.session["img_code"] = string
    # 返回一个http响应对象,类型为图片
    return HttpResponse(stream.getvalue(), content_type="image/png")

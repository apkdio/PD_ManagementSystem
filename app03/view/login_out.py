from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect

from app03.middle_things.img_code import code_img
from app03.middle_things.password import md5
from app03.models import SuperManager
from app03.view.forms import manager


def check_admin():
    if not SuperManager.objects.filter(name="admin").exists():
        SuperManager.objects.create(id=1,name="admin", password=md5("admin"))


def login(request):
    check_admin()
    ses = request.session["info"]["name"]
    if ses and SuperManager.objects.filter(name=ses).exists():
        return redirect("/depart/list/")
    if request.method == 'GET':
        form = manager()
        return render(request, 'login.html', {"form": form})
    form = manager(data=request.POST)
    if form.is_valid() == False:
        return render(request, 'login.html', {"form": form})
    code = form.cleaned_data.pop('code')
    form.cleaned_data["password"] = md5(form.cleaned_data['password'])
    user = SuperManager.objects.filter(**form.cleaned_data).first()
    if code.upper() != request.session.get("img_code", " ").upper():
        form.add_error("code", "验证码错误!")
        return render(request, 'login.html', {"form": form})
    if user is not None:
        request.session["info"] = {"id": user.id, "name": user.name}
        # 设置session超时24h
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/depart/list/')
    form.add_error("password", "用户名或者密码错误!")  # 主动增加错误信息
    return render(request, 'login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect("/main")


def image_code(request):
    img, str = code_img()
    stream = BytesIO()
    img.save(stream, 'png')
    # 将字符写入session,写入内存,不存 到项目中
    request.session["img_code"] = str
    # 返回一个http响应对象,类型为图片
    return HttpResponse(stream.getvalue(), content_type="image/png")

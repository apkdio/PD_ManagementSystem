from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app03.models import Userinfo
from app03.view.forms import user


def user_edit(request, nid):
    if nid == 24:
        return JsonResponse({"state": False}, status=403)
    if not Userinfo.objects.filter(id=nid).first():
        return JsonResponse({"state": False}, status=404)

    if request.method == "GET":
        obj = Userinfo.objects.filter(id=nid).first()
        return JsonResponse({"name": obj.name,
                             "password": obj.password,
                             "age": obj.age,
                             "account": obj.account,
                             "time": obj.time,
                             "depart": obj.depart_id,
                             "gender":obj.gender})
    instance = Userinfo.objects.get(id=nid)
    form = user(data=request.POST,instance=instance)
    if form.is_valid():
        form.save()
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})



def user_add(request):
    form = user(data=request.POST)
    if form.is_valid():
        form.save()
        """自动提交数据到数据库,相当于userinfo.objects.create
        (name=Name, age=Age, gender=Gender, password=password,
                                   depart_id=depart, account=account, time=time)"""
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})



def user_delete(request, nid):
    if nid == 24:
        return JsonResponse({"state": False}, status=404)
    Userinfo.objects.filter(id=nid).delete()
    return JsonResponse({"state": True})


def user_list(request, nid):
    form = user()
    if request.method == "GET":
        if nid == 0:
            return redirect("/user/list/1")
        else:
            start = int(nid - 1) * 8
            end = int(nid) * 8
            all = Userinfo.objects.all()[start:end]
            try:
                if all[0]:
                    pass
            except IndexError:
                msg = "该页面不存在员工数据!"
                return render(request, "error.html", {"error": msg})
            for i in all:
                try:
                    i.depart_id  # 获取数据库中的某个字符段
                    i.depart.title
                except:
                    pass  # 根据id匹配在另一张表的相应对象
            return render(request, "User_list.html", {"n1": all, "nid": nid, "form": form})
    name = request.POST.get("name")
    page_data = Userinfo.objects.filter(name=name)
    return render(request, "User_list.html", {"n1": page_data, "nid": nid})

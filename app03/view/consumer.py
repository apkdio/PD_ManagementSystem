from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app03.models import Consumer
from app03.view.forms import consumer


def consumer_list(request, nid):
    form = consumer()
    if request.method == "GET":
        if nid == 0:
            return redirect("/consumer/list/1/")
        else:
            start = int(nid - 1) * 8
            end = int(nid) * 8
            all = Consumer.objects.all()[start:end]
            try:
                if all[0]:
                    pass
            except IndexError:
                msg = "该页面不存在数据!"
                return render(request, "error.html", {"error": msg})
            for i in all:
                try:
                    i.id  # 获取数据库中的某个字符段
                    i.name
                    i.number
                    i.money
                except:
                    pass  # 根据id匹配在另一张表的相应对象
            return render(request, "consumer_list.html", {"n1": all, "nid": nid, "form": form})
    name = request.POST.get("name")
    page_data = Consumer.objects.filter(name=name)
    return render(request, "consumer_list.html", {"n1": page_data, "nid": nid, "form": form})


@csrf_exempt
def consumer_add(request):
    form = consumer(data=request.POST)
    if form.is_valid():
        form.save()
        """自动提交数据到数据库,相当于userinfo.objects.create
        (name=Name, age=Age, gender=Gender, password=password,
                                   depart_id=depart, account=account, time=time)"""
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})


def consumer_delete(request, nid):
    Consumer.objects.filter(id=nid).delete()
    return JsonResponse({"state": True})


@csrf_exempt
def consumer_edit(request, nid):
    if request.method == "GET":
        data = Consumer.objects.filter(id=nid).first()
        name = data.name
        number = data.number
        money = data.money
        return JsonResponse({"name": name, "number": number, "money": money})
    instance = Consumer.objects.get(id=nid)
    form = consumer(data=request.POST,instance=instance)
    if form.is_valid():
        form.save()
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})

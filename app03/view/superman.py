from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app03.middle_things.password import md5
from app03.models import SuperManager
from app03.view.forms import supermanager, supermanager_edit


def superman(request):
    if request.method == "GET":
        data = SuperManager.objects.all()
        form = supermanager()
        form_edit = supermanager_edit()
        return render(request, "manager.html", {"data": data, "form": form, "form_edit": form_edit})


@csrf_exempt
def superman_add(request):
    form = supermanager(data=request.POST)
    if not form.is_valid():
        return JsonResponse({"state": False, "error": form.errors})
    name = form.cleaned_data["name"]
    if SuperManager.objects.filter(name=name).exists():
        form.add_error("name", "账户名已存在!")
        return JsonResponse({"state": False, "error": form.errors})
    password = md5(form.cleaned_data["password"])
    SuperManager(name=name, password=password).save()
    return JsonResponse({"state": True})


@csrf_exempt
def superman_edit(request, nid):
    if request.method == "GET":
        if not SuperManager.objects.filter(id=nid).first():
            return JsonResponse({"state": False}, status=404)
        data = SuperManager.objects.filter(id=nid).first()
        name = data.name
        return JsonResponse({"name": name})
    form = supermanager_edit(data=request.POST)
    if form.is_valid():
        if md5(form.cleaned_data["password"]) != SuperManager.objects.get(id=nid).password:
            form.add_error("password", "与原密码不一致!")
            return JsonResponse({"state": False, "error": form.errors})
        else:
            SuperManager.objects.filter(id=nid).update(name=form.cleaned_data["name"],
                                                       password=md5(form.cleaned_data["new_password"]))
            return JsonResponse({"state": True})
    return JsonResponse({"state": False, "error": form.errors})


@csrf_exempt
def superman_delete(request, nid):
    if SuperManager.objects.filter(id=nid).first().name == "admin":
        return JsonResponse({"state": False}, status=403)
    SuperManager.objects.filter(id=nid).delete()
    return JsonResponse({"state": True})

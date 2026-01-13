from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render

from app03.middle_things.password import md5
from app03.models import SuperManager, Department, Logging
from app03.view.forms import supermanager, supermanager_edit
from example01.settings import INITIAL_SETTING

safe_password = INITIAL_SETTING['safe_password']
manage_name = INITIAL_SETTING['user']
depart_id = INITIAL_SETTING['depart_id']
normal_safe_password = INITIAL_SETTING['normal_safe_password']


def superman(request):
    if request.method == "GET":
        data = SuperManager.objects.all()
        form = supermanager()
        form_edit = supermanager_edit()
        return render(request, "manager.html", {"data": data, "form": form,
                                                "form_edit": form_edit, "manage_name": manage_name,
                                                "manage_id": depart_id})
    name = request.POST.get("name")
    page_data = SuperManager.objects.filter(name=name)
    if not list(page_data):
        page_data = None
    form = supermanager()
    return render(request, "manager.html", {"data": page_data, "form": form,
                                            "manage_id": depart_id, "person_id": request.session["info"]["id"]})


def superman_add(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    op_user = request.session["info"]["depart"]
    if op_user == depart_id:
        form = supermanager(data=request.POST)
        if not form.is_valid():
            return JsonResponse({"state": False, "error": form.errors})
        name = form.cleaned_data["name"]
        depart = form.cleaned_data["depart"]
        form.cleaned_data["password"] = md5(form.cleaned_data["password"])
        if form.cleaned_data["depart"] == Department.objects.get(id=depart_id):
            safe_password_post = request.POST.get("safe_password")
            if safe_password == safe_password_post:
                SuperManager.objects.create(name=name, password=form.cleaned_data["password"],
                                            depart=depart)
                Logging.objects.create(operate_user=request.session["info"]["name"], action="Add_manager",
                                       operate_object=({"Models": "SuperManager", "name": name, "department": depart}))
                return JsonResponse({"state": True})
            else:
                return JsonResponse({"state": False, "error": {"sp": "安全密码不正确！"}})
        else:
            if (SuperManager.objects.filter(name=name).exists() and
                    SuperManager.objects.filter(name=name).first().depart == depart):
                form.add_error("name", "同部门同用户名账号已存在!")
                return JsonResponse({"state": False, "error": form.errors})
            else:
                SuperManager.objects.create(name=name, password=form.cleaned_data["password"], depart=depart)
                Logging.objects.create(operate_user=request.session["info"]["name"], action="Add_manager",
                                       operate_object=({"Models": "SuperManager", "name": name, "department": depart}))
                return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "info": "非管理员操作！"}, status=403)


def superman_edit(request, nid):
    if request.method == "GET":
        if not SuperManager.objects.filter(id=nid).first():
            return JsonResponse({"state": False}, status=404)
        data = SuperManager.objects.filter(id=nid).first()
        name = data.name
        return JsonResponse({"name": name})
    op_user = request.session["info"]["depart"]
    if op_user == depart_id or op_user == nid:
        form = supermanager_edit(data=request.POST)
        safe_password_post = request.POST.get("safe_password")
        if form.is_valid():
            if md5(form.cleaned_data["password"]) != SuperManager.objects.get(id=nid).password:
                form.add_error("password", "与原密码不一致!")
                return JsonResponse({"state": False, "error": form.errors})
            else:
                depart = form.cleaned_data["depart"]
                if depart.id == depart_id:
                    if safe_password != safe_password_post:
                        return JsonResponse({"state": False, "error": {"sp": "安全密码不正确！"}})
                name = form.cleaned_data["name"]
                SuperManager.objects.filter(id=nid).update(name=name,
                                                           password=md5(form.cleaned_data["new_password"]),
                                                           depart_id=depart)
                Logging.objects.create(operate_user=request.session["info"]["name"], action="Update_manager",
                                       operate_object=({"Models": "SuperManager", "id": nid}))
                if form.cleaned_data["new_password"] != form.cleaned_data["password"]:
                    request.session.flush()
                    return JsonResponse({"state": True, "url": "/main"})
        return JsonResponse({"state": False, "error": form.errors})
    else:
        return JsonResponse({"state": False, "info": "非对应管理员操作！"}, status=403)


def superman_delete(request, nid):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    op_user = request.session["info"]["depart"]
    if op_user == depart_id:
        delete_name = SuperManager.objects.filter(id=nid).first().name
        if delete_name == manage_name:
            return JsonResponse({"state": False}, status=403)
        SuperManager.objects.filter(id=nid).delete()
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Delete_manager",
                               operate_object=({"Models": "SuperManager", "id": nid, "name": delete_name}))
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "info": "非管理员操作！"}, status=403)


def reset_pass(request, nid):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    sp = request.POST.get("sp")
    reset_pas = request.POST.get("reset_pass")
    if sp == normal_safe_password:
        SuperManager.objects.filter(id=nid).update(password=md5(reset_pas))
        op_user = request.session["info"]["id"]
        name = SuperManager.objects.filter(id=nid).first().name
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Reset_password",
                               operate_object=({"Models": "SuperManager", "id": nid, "name": name}))
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Session_clear_and_logout",
                               operate_object="Success")
        if op_user == nid:
            request.session.flush()
            return JsonResponse({"state": True, "url": "/main"})
        else:
            return JsonResponse({"state": True, "url": "/manager"})
    else:
        return JsonResponse({"state": False, "error": "安全密码不正确！"})

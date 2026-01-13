import json

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render

from app03.models import Department, Userinfo, Logging
from example01.settings import INITIAL_SETTING

depart_id = INITIAL_SETTING['depart_id']


def depart_list(request):
    # info=request.session["info"]["name"] 将登录的用户展现在前端
    departs = Department.objects.all()
    person = Userinfo.objects.all().values('id', 'name')
    if request.method == 'GET':
        return render(request, "depart_list.html", {"data": departs, "manage_id": depart_id, "person": person})
    name = request.POST.get("name")
    page_data = Department.objects.filter(title=name)
    if not list(page_data):
        page_data = None
    return render(request, "depart_list.html",
                  {"data": page_data, "manage_id": depart_id, "person": person})


def depart_add(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    data = json.loads(request.body.decode('utf-8'))
    op_user = request.session["info"]["depart"]
    if op_user == depart_id:
        if data.get("name"):
            title = data.get("name")
            if Department.objects.filter(title=title).exists():
                return JsonResponse({"state": False, "error": "部门已存在!"})
            Department.objects.create(title=title)
            Logging.objects.create(operate_user=request.session["info"]["name"], action="Add_department",
                                   operate_object=({"Models": "Department", "title": title}))
            return JsonResponse({"state": True})
        else:
            return JsonResponse({"state": False}, status=403)
    else:
        return JsonResponse({"state": False, "info": "非管理员操作！"}, status=403)


def depart_delete(request, nid):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    if nid == depart_id:
        return JsonResponse({"state": False}, status=403)
    op_user = request.session["info"]["depart"]
    if op_user == depart_id or op_user == nid:
        Department.objects.filter(id=nid).delete()
        title = Department.objects.filter(id=nid).first()
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Delete_department",
                               operate_object=({"Models": "Department", "id": nid, "title": title}))
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "info": "非部门管理员操作！"}, status=403)


def depart_edit(request, nid):
    if request.method == "GET":
        obj = Department.objects.filter(id=nid).first()
        return JsonResponse({"state": True, "depart_name": str(obj)})
    if nid == depart_id:
        return JsonResponse({"state": False}, status=403)
    op_user = request.session["info"]["depart"]
    if op_user == depart_id or op_user == depart_id:
        data = json.loads(request.body.decode('utf-8'))
        old_name = Department.objects.filter(id=nid).first().title
        name = data.get("new_name")
        Department.objects.filter(id=nid).update(title=name)
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Update_department",
                               operate_object=(
                                   {"Models": "Department", "id": nid, "change": str(old_name + "->" + name)}))
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "info": "非部门管理员操作！"}, status=403)


def master_set(request, nid):
    if request.method == "GET":
        data = list(Userinfo.objects.filter(depart_id=nid).values("id", "name"))
        return JsonResponse({"state": True, "data": data})
    elif request.method == "POST":
        op_user = request.session["info"]["depart"]
        if op_user == nid or op_user == depart_id:
            data = json.loads(request.body.decode('utf-8'))
            depart = data.get("depart_id")
            master_id = data.get("master")
            try:
                old_master = Userinfo.objects.filter(id=Department.objects.get(id=nid).master_id).first().name
            except:
                old_master = None
            new_master = Userinfo.objects.filter(id=master_id).first().name
            Department.objects.filter(id=depart).update(master_id=master_id)
            Logging.objects.create(operate_user=request.session["info"]["name"], action="Update_department_master",
                                   operate_object={"Models": "Department", "department": depart,
                                                   "change": str(old_master + "->" + new_master)})
            return JsonResponse({"state": True})
        else:
            return JsonResponse({"state": False, "info": "非部门管理员操作！"}, status=403)

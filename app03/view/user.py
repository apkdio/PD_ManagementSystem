from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect

from app03.models import Userinfo, Department, Logging
from app03.view.forms import user
from example01.settings import INITIAL_SETTING

depart_id = INITIAL_SETTING['depart_id']


def user_edit(request, nid):
    if request.method == "GET":
        obj = Userinfo.objects.filter(id=nid).first()
        return JsonResponse({"name": obj.name,
                             "age": obj.age,
                             "account": obj.account,
                             "time": obj.time,
                             "depart": obj.depart_id,
                             "gender": obj.gender})
    instance = Userinfo.objects.get(id=nid)
    form = user(data=request.POST, instance=instance)
    if form.is_valid():
        form.save()
        Logging.objects.create(action="Update_user", operate_object=({"Models": "Userinfo", "id": nid}),
                               operate_user=request.session["info"]["name"])
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})


def user_add(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    form = user(data=request.POST)
    if form.is_valid():
        if request.session["info"]["depart"] == depart_id:
            name = form.cleaned_data["name"]
            form.save()
        else:
            name = form.cleaned_data["name"]
            form_copy = form.save(commit=False)
            depart = request.session.get('info')["depart"]
            form_copy.depart = Department.objects.get(id=depart)
            form_copy.save()
        Logging.objects.create(action="Add_user", operate_object=({"Models": "Userinfo", "name": name}),
                               operate_user=request.session["info"]["name"])
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})


def user_delete(request, nid):
    if request.method == "GET":
        return HttpResponseNotAllowed(["GET"])
    name = Userinfo.objects.filter(id=nid).first().manage_name
    Userinfo.objects.filter(id=nid).delete()
    Logging.objects.create(action="Delete_user", operate_object=({"Models": "Userinfo", "id": nid, "name": name}),
                           operate_user=request.session["info"]["name"])
    return JsonResponse({"state": True})


def user_list(request, nid):
    form = user()
    manage_id = depart_id
    depart = request.session.get('info')["depart"]
    depart_name = Department.objects.filter(id=depart).first().title
    if request.method == "GET":
        if nid <= 0:
            return redirect("/user/list/1")
        else:
            start = int(nid - 1) * 8
            end = int(nid) * 8
            if depart is not None:
                if depart == depart_id:
                    page_data = Userinfo.objects.all()[start:end]
                else:
                    page_data = Userinfo.objects.filter(Q(depart=depart) | Q(depart=None))[start: end]
            else:
                return render(request, "User_list.html",
                              {"manage_id": manage_id, "form": form, "depart_name": depart_name})
            if not list(page_data):
                page_data = None
            return render(request, "User_list.html",
                          {"data": page_data, "manage_id": manage_id, "form": form, "depart_name": depart_name})
    name = request.POST.get("name")
    page_data = Userinfo.objects.filter(
        Q(name=name, depart=request.session["info"]["depart"]) | Q(name=name, depart=None))
    if not list(page_data):
        page_data = None
    return render(request, "User_list.html", {"data": page_data, "nid": nid,
                                              "manage_id": manage_id, "form": form, "depart_name": depart_name})

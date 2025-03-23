import json

from django.http import JsonResponse
from django.shortcuts import render


from app03.models import Departure


def depart_list(request):
    # info=request.session["info"]["name"] 将登录的用户展现在前端
    departs = Departure.objects.all()
    return render(request, "depart_list.html", {"n1": departs})



def depart_add(request):
    data = json.loads(request.body.decode('utf-8'))
    if data.get("name"):
        title = data.get("name")
        if Departure.objects.filter(title=title).exists():
            return JsonResponse({"state": False, "error": "部门已存在!"})
        Departure.objects.create(title=title)
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False},status=403)


def depart_delete(request, nid):
    if nid == 27:
        return JsonResponse({"state": False}, status=403)
    Departure.objects.filter(id=nid).delete()
    return JsonResponse({"state": True})



def depart_edit(request, nid):
    if request.method == "GET":
        obj = Departure.objects.filter(id=nid).first()
        return JsonResponse({"state": True, "depart_name": str(obj)})
    if nid == 27:
        return JsonResponse({"state": False}, status=403)
    data = json.loads(request.body.decode('utf-8'))
    name = data.get("new_name")
    Departure.objects.filter(id=nid).update(title=name)
    return JsonResponse({"state": True})

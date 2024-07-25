import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app03.models import departure


def depart_list(request):
    print(123)
    # info=request.session["info"]["name"] 将登录的用户展现在前端
    departs = departure.objects.all()
    return render(request, "depart_list.html", {"n1": departs})


@csrf_exempt
def depart_add(request):
    data = json.loads(request.body.decode('utf-8'))
    title = data.get("name")
    if departure.objects.filter(title=title).exists():
        return JsonResponse({"state": False, "error": "部门已存在!"})
    departure.objects.create(title=title)
    return JsonResponse({"state": True})


@csrf_exempt
def depart_delete(request,nid):
    if nid == 27:
        return JsonResponse({"state": False}, status=403)
    departure.objects.filter(id=nid).delete()
    return JsonResponse({"state": True})


@csrf_exempt
def depart_edit(request, nid):
    if request.method == "GET":
        obj = departure.objects.filter(id=nid).first()
        return JsonResponse({"state": True, "depart_name": str(obj)})
    if nid == 27:
        return JsonResponse({"state": False}, status=403)
    data = json.loads(request.body.decode('utf-8'))
    name = data.get("new_name")
    departure.objects.filter(id=nid).update(title=name)
    return JsonResponse({"state": True})

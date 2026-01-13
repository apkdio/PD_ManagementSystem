from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect

from app03.models import Consumer, Logging
from app03.view.forms import consumer
from example01.settings import INITIAL_SETTING

depart_id = INITIAL_SETTING['depart_id']


def consumer_list(request, nid):
    form = consumer()
    if request.method == "GET":
        if nid <= 0:
            return redirect("/consumer/list/1/")
        else:
            start = int(nid - 1) * 8
            end = int(nid) * 8
            page_data = Consumer.objects.all()[start:end]
            if not list(page_data):
                page_data = None
            return render(request, "consumer_list.html", {"data": page_data, "manage_id": depart_id, "form": form})
    name = request.POST.get("name")
    page_data = Consumer.objects.filter(name=name)
    if not list(page_data):
        page_data = None
    return render(request, "consumer_list.html", {"data": page_data, "nid": nid, "form": form,
                                                  "manage_id": depart_id})


def consumer_add(request):
    if request.method == "GET":
        return HttpResponseNotAllowed("GET")
    else:
        form = consumer(data=request.POST)
        if form.is_valid():
            form.save()
            Logging.objects.create(operate_user=request.session["info"]["name"], action="Add_consumer",
                                   operate_object={"Models": "Consumer", "name": form.cleaned_data["name"]})
            return JsonResponse({"state": True})
        else:
            return JsonResponse({"state": False, "error": form.errors})


def consumer_delete(request, nid):
    if request.method == "GET":
        return HttpResponseNotAllowed("GET")
    else:
        name = Consumer.objects.get(id=nid).manage_name
        Consumer.objects.filter(id=nid).delete()
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Delete_consumer",
                               operate_object={"Models": "Consumer", "id": nid, "name": name})
        return JsonResponse({"state": True})


def consumer_edit(request, nid):
    if request.method == "GET":
        data = Consumer.objects.filter(id=nid).first()
        name = data.name
        number = data.number
        money = data.money
        return JsonResponse({"name": name, "number": number, "money": money})
    instance = Consumer.objects.get(id=nid)
    form = consumer(data=request.POST, instance=instance)
    if form.is_valid():
        form.save()
        Logging.objects.create(operate_user=request.session["info"]["name"], action="Update_consumer",
                               operate_object={"Models": "Consumer", "id": nid})
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False, "error": form.errors})

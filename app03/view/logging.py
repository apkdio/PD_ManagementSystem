from django.http import JsonResponse
from django.shortcuts import render, redirect

from app03.models import Logging
from example01.settings import INITIAL_SETTING

depart_id = INITIAL_SETTING['depart_id']


def log(request, nid, string, name):
    action_type = Logging.objects.values_list('action', flat=True).distinct()
    if string == "all":
        if request.session["info"]["depart"] != depart_id:
            return JsonResponse({"state": False}, status=403)
        else:
            if request.method == 'GET':
                if nid <= 0:
                    return redirect('/logging/all/1/null')
                start = int(nid - 1) * 8
                end = int(nid) * 8
                page_data = Logging.objects.all().order_by("-time")[start:end]
                if list(page_data) == []:
                    page_data = None
                return render(request, 'logging.html',
                              {"data": page_data, "manage_id": depart_id, "action_type": action_type, "action": "all",
                               "name_data": "null", "nid": nid})
    elif string == "name":
        if nid <= 0:
            return redirect('/logging/all/1/null')
        if request.POST.get("name"):
            name = request.POST.get("name")
        start = int(nid - 1) * 8
        end = int(nid) * 8
        page_data = Logging.objects.filter(operate_user=name)[start:end]
        if list(page_data) == []:
            page_data = None
        return render(request, 'logging.html',
                      {"data": page_data, "manage_id": depart_id, "action_type": action_type, "action": "name",
                       "name_data": name, "nid": nid})
    elif string in list(action_type):
        if request.method == 'GET':
            if nid <= 0:
                return redirect('/logging/all/1/null')
            start = int(nid - 1) * 8
            end = int(nid) * 8
            page_data = Logging.objects.filter(action=string)[start:end]
            if list(page_data) == []:
                page_data = None
            return render(request, 'logging.html',
                          {"data": page_data, "manage_id": depart_id, "action_type": action_type, "action": string,
                           "name_data": "null", "nid": nid})
        else:
            return JsonResponse({"state": False}, status=404)

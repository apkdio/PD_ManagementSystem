from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from app03.models import SuperManager


# 中间件 #1
class Justice(MiddlewareMixin):
    # 在每次request,执行到相对应视图函数前执行
    def process_request(self, request):
        if request.path_info in "/":
            return redirect("/main")
        if request.path_info in ["/main", "/main/", "/code/img", "/code/img/"]:
            return None
        if request.session or request.session.get("info"):
            name = request.session["info"]["name"]
            if not SuperManager.objects.filter(name=name):
                return redirect("/main")
            return None
        return redirect("/main")

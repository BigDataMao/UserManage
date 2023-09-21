from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from users import models
from users.utils.bootstrap import BootstrapModelForm


class TaskFrom(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


def task_list(request):
    return render(request, "task_list.html")


@csrf_exempt
def task_ajax(request):
    a = request.GET.get("a")
    print(a)
    return HttpResponse(a)

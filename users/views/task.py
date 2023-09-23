from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from users import models
from users.utils.bootstrap import BootstrapModelForm


class TaskForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "task_content": forms.TextInput(attrs={"class": "form-control"}),
        }


def task_list(request):
    task_form = TaskForm()
    tasks = models.Task.objects.all()
    return render(request, "task_list.html", {"form": task_form, "tasks": tasks})


@csrf_exempt
def task_ajax(request):
    a = request.GET.get("a")
    print(a)
    return HttpResponse(a)


@csrf_exempt
def task_submit(request):
    task_form = TaskForm(request.POST)
    print(task_form)
    if task_form.is_valid():
        task_form.save()
        return HttpResponse("ok")


@csrf_exempt
def task_delete(request):
    task_id = request.POST.get("task_id")
    print(task_id, type(task_id))
    try:
        task = models.Task.objects.get(id=task_id)
        task.delete()
        return HttpResponse("ok")
    except:
        return HttpResponse("删除失败")

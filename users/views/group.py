from django.shortcuts import render, redirect

from users import models
from users.utils.form import GroupForm


# Create your views here.
def group_list(request):
    groups = models.Group.objects.all()
    return render(request, "group_list.html", {"groups": groups})


def group_add(request):
    if request.method == "GET":
        group_form = GroupForm()
        return render(request, "group_add.html", {"group_form": group_form})
    # 获取用户提交的数据
    group_form = GroupForm(request.POST)
    # 校验数据
    if group_form.is_valid():
        # 保存数据
        group_form.save()
        # 跳转到用户组列表页面
        return redirect("/group/list/")


def group_edit(request, group_id):
    # 获取要编辑的用户组对象
    group = models.Group.objects.get(id=group_id)
    if request.method == "GET":
        # 将用户组对象传递给前端页面
        group_form = GroupForm(instance=group)
        return render(request, "group_edit.html", {"group_form": group_form})
    # 获取用户提交的数据
    group_form = GroupForm(request.POST, instance=group)
    # 校验数据
    if group_form.is_valid():
        # 亦可自定义一些数据
        # group_form.instance.group_name = "自定义"
        # 保存数据
        group_form.save()
        # 跳转到用户组列表页面
        return redirect("/group/list/")
    # 校验失败，group_form.errors会带上错误信息
    return render(request, "group_edit.html", {"group_form": group_form})


def group_delete(request, group_id):
    # 获取要删除的用户组对象
    group = models.Group.objects.get(id=group_id)
    # 删除用户组
    group.delete()
    # 跳转到用户组列表页面
    return redirect("/group/list/")
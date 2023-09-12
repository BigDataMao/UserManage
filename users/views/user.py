from django.shortcuts import render, redirect

from users import models
from users.utils.form import UserForm


def user_list(request):
    users = models.User.objects.all()
    return render(request, "user_list.html", {"users": users})


def user_add(request):
    if request.method == "GET":
        user_form = UserForm()
        return render(request, "user_add.html", {"user_form": user_form})
    # 获取用户提交的数据
    user_form = UserForm(request.POST)
    # 校验数据
    if user_form.is_valid():
        # 保存数据
        user_form.save()
        # 跳转到用户列表页面
        return redirect("/user/list/")


def user_edit(request, user_id):
    # 获取要编辑的用户对象
    user = models.User.objects.get(id=user_id)
    if request.method == "GET":
        # 将用户对象传递给前端页面
        user_form = UserForm(instance=user)
        return render(request, "user_edit.html", {"user_form": user_form})
    # 获取用户提交的数据
    user_form = UserForm(request.POST, instance=user)
    # 校验数据
    if user_form.is_valid():
        # 亦可自定义校验规则
        if user_form.cleaned_data["username"] == "admin":
            user_form.add_error("username", "用户名不能为admin,你怕是要卡bug吗")
            return render(request, "user_edit.html", {"user_form": user_form})
        # 亦可制造埋点数据
        # user_form.instance.xxx = "123456"
        # 保存数据
        user_form.save()
        # 跳转到用户列表页面
        return redirect("/user/list/")
    # 校验失败，user_form.errors会带上错误信息
    return render(request, "user_edit.html", {"user_form": user_form})


def user_delete(request, user_id):
    # 获取要删除的用户对象
    user = models.User.objects.get(id=user_id)
    # 删除用户
    user.delete()
    # 跳转到用户列表页面
    return redirect("/user/list/")
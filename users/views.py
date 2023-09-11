from django.shortcuts import render, redirect
from users import models
from django import forms


# Create your views here.
def test(request):
    return render(request, "test.html")


def group_list(request):
    groups = models.Group.objects.all()
    return render(request, "group_list.html", {"groups": groups})


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        # fields = "__all__"  # 所有字段
        fields = ["group_name"]

    # 重写__init__方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个字段添加样式
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = f"请输入{field.label}"


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


def user_list(request):
    users = models.User.objects.all()
    return render(request, "user_list.html", {"users": users})


class UserForm(forms.ModelForm):
    # xx = forms.CharField(label="自定义")  # 自定义字段xx
    class Meta:
        model = models.User
        # fields = "__all__"  # 所有字段
        fields = ["username", "password", "email", "gender", "birthday", "account", "vip_end_time", "group"]

    # 重写__init__方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个字段添加样式
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = f"请输入{field.label}"


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

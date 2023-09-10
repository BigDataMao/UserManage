from django.shortcuts import render, redirect
from users import models


# Create your views here.
def test(request):
    return render(request, "test.html")


def group_list(request):
    groups = models.Group.objects.all()
    return render(request, "group_list.html", {"groups": groups})


def user_list(request):
    users = models.User.objects.all()
    return render(request, "user_list.html", {"users": users})


from django import forms


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


def user_delete(request, user_id):
    # 获取要删除的用户对象
    user = models.User.objects.get(id=user_id)
    # 删除用户
    user.delete()
    # 跳转到用户列表页面
    return redirect("/user/list/")
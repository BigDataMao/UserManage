from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect

from users import models
from users.utils.code import check_code
from users.utils.form import AdminForm, AdminFormEdit, AdminFormReset, LoginForm


# Create your views here.
def admin_list(request):
    admins = models.Admin.objects.all()
    return render(request, "admin_list.html", {"admins": admins})


def admin_add(request):
    title = "管理员账户添加"

    if request.method == "GET":
        admin_form = AdminForm()
        return render(request, "common_change.html", {"form": admin_form, "title": title})
    # 获取用户提交的数据
    admin_form = AdminForm(data=request.POST)
    # 校验数据
    if admin_form.is_valid():
        # 保存数据
        admin_form.save()
        # 跳转到用户组列表页面
        return redirect("/admin/list/")
    # 校验失败，admin_form.errors会带上错误信息
    return render(request, "common_change.html", {"form": admin_form, "title": title})


def admin_edit(request, admin_id):
    admin_name = models.Admin.objects.get(id=admin_id).username
    title = f"管理员名字修改:原名--{admin_name}"
    if request.method == "GET":
        # 将用户组对象传递给前端页面
        admin_form_edit = AdminFormEdit()
        return render(request, "common_change.html", {"form": admin_form_edit, "title": title})
    # 获取用户提交的数据
    admin_form_edit = AdminFormEdit(data=request.POST)
    # 校验数据
    if admin_form_edit.is_valid():
        # 修改数据
        admin = models.Admin.objects.get(id=admin_id)
        admin.username = admin_form_edit.cleaned_data.get("username")
        admin.save()
        # 跳转到用户组列表页面
        return redirect("/admin/list/")
    # 校验失败，admin_form.errors会带上错误信息
    return render(request, "common_change.html", {"form": admin_form_edit, "title": title})


def admin_delete(request, admin_id):
    models.Admin.objects.get(id=admin_id).delete()
    return redirect("/admin/list/")


def admin_reset(request, admin_id):
    name = models.Admin.objects.get(id=admin_id).username
    title = f"密码重置--{name}"
    if request.method == "GET":
        admin_form_reset = AdminFormReset()
        return render(request, "common_change.html", {"form": admin_form_reset, "title": title})
    # 获取用户提交的数据
    admin_form_reset = AdminFormReset(data=request.POST, instance=models.Admin.objects.get(id=admin_id))
    # 校验数据
    if admin_form_reset.is_valid():
        # 修改数据
        admin_form_reset.save()
        # 跳转到用户组列表页面
        return redirect("/admin/list/")
    # 校验失败，admin_form.errors会带上错误信息
    return render(request, "common_change.html", {"form": admin_form_reset, "title": title})


def login(request):
    """ 登录 """
    # 判断用户是否已经登录
    if request.session.get("username"):
        return redirect("/admin/list/")
    # 未登录则跳转到登录页面
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "login.html", {"form": login_form})
    # 获取用户登录数据
    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
        # 校验验证码
        user_input_code = login_form.cleaned_data.pop('image_code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            login_form.add_error("image_code", "验证码错误")
            return render(request, 'login.html', {'form': login_form})
        # 校验用户名和密码
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        if models.Admin.objects.filter(username=username, password=password).exists():
            request.session["username"] = username
            return redirect("/admin/list/")
        else:
            login_form.add_error("username", "用户名或密码错误")
            return render(request, "login.html", {"form": login_form})
    return render(request, "login.html", {"form": login_form})


def logout(request):
    """ 登出 """
    request.session.flush()
    return redirect("/login/")


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

from django import forms
from django.core.exceptions import ValidationError

from users import models
from users.utils.bootstrap import BootstrapModelForm
from users.utils.encrypt import md5


class GroupForm(BootstrapModelForm):
    class Meta:
        model = models.Group
        # fields = "__all__"  # 所有字段
        fields = ["group_name"]


class UserForm(BootstrapModelForm):
    # xx = forms.CharField(label="自定义")  # 自定义字段xx
    class Meta:
        model = models.User
        # fields = "__all__"  # 所有字段
        fields = ["username", "password", "email", "gender", "birthday", "account", "vip_end_time", "group"]


class AdminForm(BootstrapModelForm):
    password_confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        """给 password 字段进行MD5加密"""
        password = self.cleaned_data.get("password")
        return md5(password)

    def clean_password_confirm(self):
        """在 Django 的表单验证中，clean_<field_name> 方法是 Django 自动调用的"""
        password = self.cleaned_data.get("password")
        password_confirm = md5(self.cleaned_data.get("password_confirm"))
        if password != password_confirm:
            raise ValidationError("两次密码不一致")
        return password_confirm


class AdminFormEdit(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username", ]

    def clean_username(self):
        """给 username 字段进行校验"""
        username = self.cleaned_data.get("username")
        if username == "root":
            raise ValidationError("用户名不能为root")
        return username


class AdminFormReset(BootstrapModelForm):
    password_confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["password", "password_confirm"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        """给 password 字段进行MD5加密"""
        password = md5(self.cleaned_data.get("password"))
        # 校验密码不能跟原密码一致
        if password == models.Admin.objects.get(id=self.instance.pk).password:
            raise ValidationError("新密码不能与原密码一致")
        return password

    def clean_password_confirm(self):
        """在 Django 的表单验证中，clean_<field_name> 方法是 Django 自动调用的"""
        password = self.cleaned_data.get("password")
        password_confirm = md5(self.cleaned_data.get("password_confirm"))
        if password != password_confirm:
            raise ValidationError("两次密码不一致")
        return password_confirm


class LoginForm(BootstrapModelForm):
    image_code = forms.CharField(label="验证码", widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = models.Admin
        fields = ["username", "password", "image_code"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        """给 password 字段进行MD5加密"""
        password = self.cleaned_data.get("password")
        return md5(password)

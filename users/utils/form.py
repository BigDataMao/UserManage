from users import models
from users.utils.bootstrap import BootstrapModelForm


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
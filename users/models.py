from django.db import models

# Create your models here.
"""
数据库生成命令:
python manage.py makemigrations
python manage.py migrate
"""


class Group(models.Model):
    """区分各用户组的功能"""
    group_name = models.CharField(max_length=32, verbose_name="用户组名称")

    # 定义返回值
    def __str__(self):
        return self.group_name


class User(models.Model):
    """用户类"""
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    gender_choices = (
        (0, "女"),
        (1, "男"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    birthday = models.DateField(verbose_name="生日")
    account = models.IntegerField(verbose_name="账户余额", default=0)
    vip_end_time = models.DateTimeField(verbose_name="会员到期时间")
    group = models.ForeignKey(to="Group", to_field="id", verbose_name="用户组",
                              null=True, blank=True, on_delete=models.CASCADE)

    # 定义年龄方法
    def get_age(self):
        import datetime
        return int((datetime.datetime.now().date() - self.birthday).days / 365.25)

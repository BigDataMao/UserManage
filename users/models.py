from django.db import models

# Create your models here.
"""
数据库生成命令:
python manage.py makemigrations
python manage.py migrate
"""


class Admin(models.Model):
    """管理员类"""
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")

    # 定义返回值
    def __str__(self):
        return self.username


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


class Task(models.Model):
    """任务类"""
    level_choices = (
        (0, "简单"),
        (1, "中等"),
        (2, "困难"),
    )
    task_level = models.SmallIntegerField(verbose_name="任务等级", choices=level_choices)
    task_manager = models.ForeignKey(to="Admin", to_field="id", verbose_name="任务负责人", on_delete=models.CASCADE)
    task_name = models.CharField(max_length=32, verbose_name="任务名称")
    task_content = models.TextField(verbose_name="任务内容")


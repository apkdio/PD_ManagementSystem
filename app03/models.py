from django.db import models


class Departure(models.Model):
    title = models.CharField(verbose_name="部门", max_length=16)

    # verbose_name 是该元素在Django后台显示的名称,传输到model_form里作默认名称

    # 当网站上显示为对象+类名的时候可以重写该函数解决
    def __str__(self):
        return self.title


class Userinfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=20)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="月薪", max_digits=10, decimal_places=2,
                                  default=0)
    time = models.DateField(verbose_name="入职时间")
    """MySQL中的约束"""
    """以下语句中的on_delete是MySQL中的行为,与Django无关"""
    depart = models.ForeignKey(verbose_name="部门", to="app03.Departure", null=True, blank=True,
                               on_delete=models.SET_NULL)  # 滞空处理,当外键被删除时自动设置成null
    # 还有一种级联方式,当外键的数据被删除时连带外键所在的数据一块删除,此时on_delete=models.CASCADE
    # to 表,to_field 表的某一列
    # 该命令会生成depart_id列
    """Django中的约束"""
    """以下代码中的choice是Django做出的行为,与MySQL无关"""
    gender_choice = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)


class SuperManager(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=30)
    password = models.CharField(verbose_name="密码", max_length=60)


class Consumer(models.Model):
    name = models.CharField(verbose_name="客户姓名",max_length=30)
    number = models.IntegerField(verbose_name="客户电话")
    money = models.DecimalField(verbose_name="客户余额",max_digits=20,decimal_places=2,default=0)

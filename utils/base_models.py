from django.db import models


class BaseModel(models.Model):
    # 输出时间
    creat_time = models.DateTimeField(auto_now_add=True)
    updata_time = models.DateTimeField(auto_now=True)

    # abstract = True则进行数据库迁移时，不会创建BaseModel这张表
    class Meta:
        abstract = True

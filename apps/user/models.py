from django.db import models
# from utils.base_models import BaseModel
#
#
# class Tb_Users(BaseModel):
#     id = models.AutoField(primary_key=True)
#     password = models.CharField(max_length=128, verbose_name='密码', help_text='密码', unique=True)
#     username = models.CharField(max_length=150, verbose_name='账户', help_text='账户')
#     first_name = models.CharField(max_length=30, verbose_name='姓氏', help_text='姓氏')
#     last_name = models.CharField(max_length=150, verbose_name='名字', help_text='名字')
#     email = models.CharField(max_length=254, verbose_name='邮件地址', help_text='邮件地址')
#     is_staff = models.IntegerField(verbose_name='是否为管理员', help_text='是否为管理员')
#     is_superuser = models.IntegerField(verbose_name='是否为超级管理员', help_text='是否为超级管理员')
#     is_active = models.IntegerField(verbose_name='是否活跃', help_text='是否活跃')
#     last_login = models.DateTimeField(auto_now=True, verbose_name='最后一次登陆时间', help_text='最后一次登陆时间')
#
#     class Meta:
#         db_table = 'tb_users'
#         verbose_name = '用户表'

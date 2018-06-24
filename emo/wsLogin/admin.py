from django.contrib import admin
from wsLogin.models import WxUser, WxOpenid

# Register your models here.
admin.site.register(WxUser)
admin.site.register(WxOpenid)
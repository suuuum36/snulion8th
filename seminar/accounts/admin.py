from django.contrib import admin
from .models import Profile  #models.py에서 feed 모델을 사용한다!

# Register your models here.
admin.site.register(Profile)
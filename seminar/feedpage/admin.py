from django.contrib import admin
from .models import Feed, FeedComment, Like  #models.py에서 feed 모델을 사용한다!

# Register your models here.
admin.site.register(Feed)
admin.site.register(FeedComment)
admin.site.register(Like)

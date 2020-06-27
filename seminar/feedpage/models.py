# seminar/feedpage/models.py
from django.db import models
from django.utils import timezone # 장고는 created_at과 updated_at을 알아서 만들어 주지 않음. id는 만들어 줌
from django.contrib.auth.models import User
from django.apps import apps

# Create your models here.
class Feed(models.Model): # 모델 클래스명은 단수형을 사용 (Feeds(x) Feed(O))
    # id는 자동 추가
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE) 
    liked_users = models.ManyToManyField(User, blank=True, related_name='feeds_liked', through='Like')

    def update_date(self): # 나중에 수정할 때 사용
        self.updated_at = timezone.now()
        self.save()

    #데이터를 보기 쉽게 정렬해주는 매소드.
    def __str__(self):
        return self.title  #위의 title 객체를 정렬해 보여준다는 뜻

class FeedComment(models.Model):
    content = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(User, blank=True, related_name='comments_liked', through='CommentLike')

    def __str__(self):
        return str(self.id)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Follow(models.Model): 
    follow_to = models.ForeignKey('accounts.Profile', related_name = 'follow_to', on_delete=models.CASCADE)
    follow_from = models.ForeignKey('accounts.Profile', related_name = 'follow_from', on_delete=models.CASCADE)

    def __str__(self):
        return '{} follows {}'.format(self.follow_from, self.follow_to)
    
class CommentLike(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(FeedComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
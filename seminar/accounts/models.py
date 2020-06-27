from django.db import models
from django.utils import timezone
from faker import Faker # -> fake 데이터 생성해주는 기능
from django.contrib.auth.models import User #-> 장고 기본 내장된 user 모델 사용한다고 명시
from django.db.models.signals import post_save  
from django.dispatch import receiver

# One-to-One field로 profile 모델을 만들어주고 User을 연결
# 하나의 profile 모델은 하나의 user 모델 가지게 됨.

class Profile(models.Model): 
    
    # profile1.user = user1 / user1.profile = profile1
    # on_delete = if user1 deleted, profile1 deleted simultaneously
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=20, blank=True)
    follows = models.ManyToManyField('self', through = 'feedpage.Follow', blank=True, related_name = 'followed', symmetrical=False)
    
    # python formatting : %d = 정수 삽입 / %s = 문자열 삽입
    def __str__(self): 
        return 'id=%d, user_id=%d, college=%s, major=%s, age=%s' % (self.id, self.user.id, self.college, self.major, self.age)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):  
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):  
        instance.profile.save()
    
    
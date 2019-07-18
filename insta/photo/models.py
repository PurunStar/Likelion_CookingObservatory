from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Photo(models.Model):
    # 유저이름가져오기
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='timeline_photo/%Y/%m/%d')  # 알아서 등록날자를 적어
    created = models.DateTimeField(auto_now_add=True)  # 지금생성시간저장
    updated = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(
        User, related_name='favorite_post', blank=True)

    def __str__(self):
        return "text : "+self.text

    class Meta:
        ordering = ['-created']  # 정렬방식 : -최신순 그냥은 오래된순

    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id])

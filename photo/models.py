from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    title = models.CharField(max_length=20 ,null=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')  # 알아서 등록날자를 적어
    image2 = models.ImageField(blank=True,null=True, upload_to='timeline_photo/%Y/%m/%d')
    image3 = models.ImageField(blank=True, null=True,upload_to='timeline_photo/%Y/%m/%d')
    hit_count_generic = GenericRelation( HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    #크기 줄이는게 아닌데 ?? 
    image_thumbnail = ImageSpecField(source = 'image', processors = [ResizeToFill(300, 300)])
    image_thumbnail = ImageSpecField(source = 'image2', processors = [ResizeToFill(300, 300)])
    image_thumbnail = ImageSpecField(source = 'image3', processors = [ResizeToFill(300, 300)])
    
    #객체가 처음 생성될 때 시간정보 저장
    created = models.DateTimeField(auto_now_add=True, null=True)
    #객체가 저장될 때마다 자동으로 시간 저장
    updated = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='like_post', blank=True)

    #제목 그래도 출력
    def __str__(self):
        return  self.text

    def summary(self) : 
        return self.text[0:17]

    def len(self) :
        text_len = len(self.text)
        return text_len

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self) : 
        return reverse('photo:detail', args=[self.id])

class Comment(models.Model) : 
    post = models.ForeignKey(Photo, on_delete = models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete = models.CASCADE) 
    body = models.CharField(max_length=500)
    date = models.DateTimeField('date published')
    
    def __str__(self) :
        return self.body




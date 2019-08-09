from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse

from .models import Photo
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User

from django.core.paginator import Paginator

from .models import Photo
from .models import Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from hitcount.views import HitCountDetailView

#mylist
class PhotoMylist(ListView) :
    model = Photo
    template_name = 'photo/photo_mylist.html'

    def dispatch(self, request, *args, **kwargs) :
        #로그인 확인
        if not request.user.is_authenticated :
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMylist, self).dispatch(request, *args, **kwargs)

#좋아요
class PhotoLike(View) :
    def get(self, request, *args, **kwargs) : 
        #로그인 확인 = 로그인안된 상태이면 자료를 숨김
        if not request.user.is_authenticated : 
            return HttpResponseForbidden()
        else :
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                #이미 좋아요를 누른 상태에서 다시 누르면 좋아요 취소
                if user in photo.like.all():
                    photo.like.remove(user)
                else : 
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)                 


#class형 뷰의 generic view를 이용하여 구현 
#PhotoList 가장 메인에서 보여줄 로직 
class PhotoList(ListView) : 
    model = Photo
    template_name = 'photo/base.html'
    #한 페이지 그룹의 페이지 수
    paginate_by = 6

    def get_context_data(self, **kwargs):
        global page
        context = super(PhotoList, self).get_context_data(**kwargs)
        paginator = context['paginator']

        #5개씩 잘라서 보여줌
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class PhotoCreate(CreateView) : 
    model = Photo
    fields = ['title', 'text' , 'image','image2','image3']
    template_name_suffix = '_create'
    #성공하면 메인 페이지로 이동하기 위해 url을 '/'로 설정
    success_url ='/'
    #user_id확인
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.autor_id = self.request.user.id
        if form.is_valid() :
            #올바르다면
            form.instance.save()
            return redirect('/photo')
        else : 
            #올바르지 않다면
            return self.render_to_response({'form' : form})

class PhotoUpdate(UpdateView) : 
    model = Photo
    fields = ['title', 'text' , 'image','image2','image3']
    template_name_suffix = '_update'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        id = object.id
        if object.author != request.user :
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('')
        else :  
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)
        success_url = ('/photo/detail/' + str(id))

class PhotoDelete(DeleteView) : 
    model = Photo
    template_name_suffix = '_delete'
    success_url ='/photo'

    def dispatch(self, request, *args, **kwargs) : 
        object = self.get_object()
        if object.author != request.user :
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else : 
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView) : 
    model = Photo

    def get_context_data(self, **kwargs):
        context = super(PhotoDetail, self).get_context_data(**kwargs)
        context['photo_list'] = Photo.objects.all()
        return context

class PostCountHitDetailView(PhotoDetail, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True

@login_required
def comment_add(request, photo_id) :
    if request.method == "POST" :
        post = get_object_or_404(Photo, pk=photo_id)
        comment = Comment()
        comment.user = request.user
        comment.body = request.POST['body']
        comment.post = post
        comment.date = timezone.now()
        comment.save()
        return redirect('/photo/detail/' + str(photo_id))
    else :
        return HttpResponse('잘못된 접근입니다.')


def comment_edit(request, comment_id) : 
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user :
        if request.method == "POST" :
            comment.body = request.POST['body']
            comment.save()
            return redirect('/photo/detail/' + str(comment.post.id))
        elif request.method == "GET" :
            context ={
                'comment' : comment
            }  
            return render(request, 'photo/comment_edit.html', context)
    else :
        return HttpResponse('잘못된 접근입니다.')


def comment_delete(request, comment_id) :
    comment = get_object_or_404(Comment, pk = comment_id)
    if request.user == comment.user:
        if request.method == "POST": 
            comment.delete()
            return redirect('/photo/detail/' +str(comment.post.id ))
    return HttpResponse('잘못된 접근입니다.')

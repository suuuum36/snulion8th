# seminar/feedpage/views.py
from django.shortcuts import render
from .models import Feed, FeedComment, Like, Follow
from accounts.models import Profile
from django.shortcuts import redirect 
from django.contrib.auth.models import User  
from django.db.models import Count

def index(request): # 원래 있던 index 함수 수정.
    if request.method == 'GET':
        feeds = Feed.objects.all()
        return render(request, 'feedpage/index.html', {'feeds': feeds})
    
    elif request.method == 'POST': # create(form을 이용하여 submit한 형태)
        title = request.POST['title']
        content = request.POST['content']
        Feed.objects.create(title=title, content=content, author = request.user)
        return redirect('/feeds') 
        
def new(request):
    return render(request, 'feedpage/new.html')

#url에 있는 int:id 중에서 id를 호출해야함
def show(request,id):   
    if request.method == 'GET':
        feed=Feed.objects.get(id=id)
        return render(request,'feedpage/show.html',{'feed':feed})
    elif request.method == 'POST':
        feed=Feed.objects.get(id=id)
        feed.title=request.POST['title']
        feed.content=request.POST['content']
        feed.save()
        feed.update_date()
        return redirect('/feeds/'+str(id)) 
    
def delete(request,id):
    feed=Feed.objects.get(id=id)
    feed.delete()
    return redirect('/feeds')
    

def edit(request, id):
    # if request.method == 'GET':
        feed = Feed.objects.get(id=id)
        return render(request, 'feedpage/edit.html', {'feed': feed})
    
    # elif request.method == 'POST':
    #     feed=Feed.objects.get(id=id)
    #     feed.title=request.POST['title']
    #     feed.content=request.POST['content']
    #     feed.save()
    #     feed.update_date()
    #     return redirect('/feeds/'+str(id)) 
    
def create_comment (request, id):
    content = request.POST['content']
    feed = Feed.objects.get(id=id)
    FeedComment.objects.create(feed=feed, content=content, author = request.user)
    return redirect ('/feeds')

def delete_comment (request, id, cid):
    c = FeedComment.objects.get(id=cid)
    c.delete()
    return redirect ('/feeds')

def feed_like (request, pk):
    feed = Feed.objects.get(id = pk)
    like_list = feed.like_set.filter(user_id = request.user.id)
    if like_list.count() > 0:
        feed.like_set.get(user_id = request.user.id).delete()
    else:
        Like.objects.create(user_id = request.user.id, feed_id = feed.id)
    return redirect ('/feeds')

def follow_manager(request, pk):
    follow_from = Profile.objects.get(user_id = request.user.id)
    follow_to = Profile.objects.get(user_id = pk)

    try:
        following_already = Follow.objects.get(follow_from=follow_from, follow_to=follow_to)
    
    #following_already의 값이 None이 아니라면, else-> 
    except Follow.DoesNotExist:
        following_already = None

    if following_already:
        following_already.delete()
        
    else:
        # Follow.objects.create(follow_from=follow_from, follow_to=follow_to)
        f = Follow()
        f.follow_from, f.follow_to = follow_from, follow_to
        f.save()
    return redirect('/feeds')

def comment_like(request, id, cpk):
    comment = FeedComment.objects.get(id=cpk)
    like_list = comment.commentlike_set.filter(user_id=request.user.id)    
    if like_list.count() > 0:
        comment.commentlike_set.get(user_id = request.user.id).delete()
        
    else :
        CommentLike.objects.create(user_id=request.user.id, comment_id = comment.id)

    return redirect ('/feeds')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm

# Create your views here.
def post_list(request):
    post = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {"posts":post})


def post_details(request,  pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_details.html", {"posts":post})

def post_new(request):
    # print(request.method) on first reload method is by default always get
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) #saving form but not saving it in database; .save return a model
            post.author = request.user
            post.published_date =  timezone.now()
            post.save()
            return redirect('post_details', pk=post.pk)
    form = PostForm()
    return render(request, "blog/post_edit.html", {"form":form})

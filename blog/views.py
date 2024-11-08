from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = '../templates/blog/post/list.html'


# def post_list(request):
#     posts_list = Post.published.all()
#     #Постраничная разбивка с 5 постами на страницу
#     paginator=Paginator(posts_list, 5)
#     page_number=request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если page_number находится вне диапазона, то
#         # выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   '../templates/blog/post/list.html',
#                   {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  '../templates/blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


class BlogCreateView(CreateView):
    model = Post
    template_name = '../templates/blog/post/post_new.html'
    fields = ['title', 'author', 'body', 'status']


# class BlogUpdateView(UpdateView):
#     model = Post
#     template_name = '../templates/blog/post/post_edit.html'
#     fields = ['title', 'body']

def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "Post":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\s comments: {cd['comments']}"
            send_mail(subject, message, 'shohbaron980@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,
                  '../templates/blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=require_POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,
                  '../templates/blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})

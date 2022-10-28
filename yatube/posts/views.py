from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from core.utils import paginate
from posts.forms import PostForm
from posts.models import Group, Post, User


def index(request):
    page_obj = paginate(
        request, settings.POSTS_NUMBER,
        Post.objects.select_related('group', 'author').all(),
    )
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': page_obj,
        },
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_obj = paginate(
        request, settings.POSTS_NUMBER,
        group.posts.select_related('author').all(),
    )
    return render(
        request,
        'posts/group_list.html',
        {
            'group': group,
            'page_obj': page_obj,
        },
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author', 'group')
    posts_count = posts.count()
    page_obj = paginate(request,
                        settings.POSTS_NUMBER,
                        author.posts.select_related('author', 'group')
                        )
    context = {
        'author': author,
        'posts_count': posts_count,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
        },
    )


@login_required
def post_create(request):
    group = Group.objects.all()
    form = PostForm(request.POST or None)
    if request.method != 'POST' or not form.is_valid():
        form = PostForm(None)
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
                'group': group,
            },
        )
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', request.user)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user.id != post.author.id:
        return redirect("posts:post_detail", post.pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
        form.save()
        return redirect('posts:post_detail', post_id)

    context = {'form': form, 'is_edit': True, 'post': post}
    return render(request, 'posts/create_post.html', context)

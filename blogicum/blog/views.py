from django.shortcuts import (
    render, get_object_or_404, redirect
)
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from .constants import PAGINATION


def profile_view(request, username=None):
    """Профиль пользователя."""
    if username is None:
        username = request.user.username

    user = get_object_or_404(User, username=username)

    # Получаем посты с количеством комментариев
    posts = user.posts.all().annotate(
        comment_count=Count('comments')).order_by('-pub_date')

    paginator = Paginator(posts, PAGINATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/profile.html', {'profile': user,
                                                 'page_obj': page_obj})


@login_required
def edit_profile(request):
    """Редактирование пользователя."""
    form = UserChangeForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    """Создание поста."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form})


@login_required
def edit_post(request, post_id):
    """Изменение поста."""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


def filter_published_posts(queryset):
    """Возвращает отфильтрованный queryset для опубликованных постов."""
    return queryset.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True,
    )


def index(request):
    """Главная страница, выводит список публикаций."""
    posts = filter_published_posts(Post.objects.all()).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    paginator = Paginator(posts, PAGINATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    """Детализация по посту."""
    post = get_object_or_404(Post, id=post_id)

    # Проверка авторства
    if post.author != request.user:
        # Если это не ваш пост, показываем только опубликованный пост
        post = get_object_or_404(
            filter_published_posts(Post.objects.all()), pk=post_id)

    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'form': form,
        'comments': comments,
    })


def category_posts(request, category_slug):
    """Страница категории, выводит все посты для данной категории."""
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    posts = filter_published_posts(category.posts.all())
    paginator = Paginator(posts, PAGINATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, 'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def register(request):
    """Регистрация пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,
                  'registration/registration_form.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Удаление поста."""
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)

    post.delete()
    return redirect('blog:index')


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментарий."""
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment.html', {
        'post': post,
        'form': form,
        'comment': comment,
        'comments': post.comments.all(),
    })


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post.id)
    return render(request, 'blog/comment.html', context={'comment': comment})

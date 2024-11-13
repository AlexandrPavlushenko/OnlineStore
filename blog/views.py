from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(View):
    def get(self, request):
        posts = BlogPost.objects.filter(is_published=True)
        return render(request, 'blog/post_list.html', {'posts': posts, 'title': 'Список постов'})


class BlogPostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        post.views_count += 1
        post.save()
        return render(request, 'blog/post_detail.html', {'post': post, 'title': f'Пост #{pk}'})


class BlogPostCreateView(View):
    def get(self, request):
        form = BlogPostForm()
        return render(request, 'blog/post_form.html', {'form': form, 'title': 'Создать пост'})

    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')  # Перенаправление на список постов
        return render(request, 'blog/post_form.html', {'form': form})


class BlogPostUpdateView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        form = BlogPostForm(instance=post)
        return render(request, 'blog/post_form.html', {'form': form, 'title': f'Редактировать пост #{pk}'})

    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)  # Перенаправление на детальную страницу поста
        return render(request, 'blog/post_form.html', {'form': form})


class BlogPostDeleteView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        post.delete()
        return redirect('blog:post_list')  # Перенаправление на список постов

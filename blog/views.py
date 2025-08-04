from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Post, Category, Tag


def post_list(request):
    """Display a list of published posts with pagination."""
    posts = Post.objects.filter(status='published')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Display a single post with comments."""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """Display posts from a specific category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Display posts with a specific tag."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tag_posts.html', context)


def about(request):
    """About page."""
    return render(request, 'blog/about.html')


def contact(request):
    """Contact page."""
    return render(request, 'blog/contact.html')

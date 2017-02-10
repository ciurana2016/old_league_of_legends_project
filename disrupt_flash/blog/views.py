from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import BlogPost


class BlogPostView( DetailView ):
	template_name = 'blog/blog_post.html'
	model = BlogPost


class BlogPostsView( ListView ):
	template_name = 'blog/blog_posts.html'
	model = BlogPost
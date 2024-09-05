from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from api.serializers import PostSerializer, CommentSerializer

class HomeView(APIView):
    def get(self, request):
        posts = Post.published.all()
        ser_data = PostSerializer(posts, many=True)
        return Response(ser_data.data)

class PostDetailView(APIView):
    def get(self, request, year, month, day, slug):
        post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=slug,
                            publish__year=year,  
                            publish__month=month,
                            publish__day=day)
        
        ser_data_post = PostSerializer(post)

        comment = post.comments.filter(active=True)
        ser_data_comment = CommentSerializer(comment, many=True)
        
        return Response({
            "post": ser_data_post.data,
            "comments": ser_data_comment.data,
        })
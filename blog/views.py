from django.shortcuts import render
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from api.serializers import PostSerializer

class HomeView(APIView):
    def get(self, request):
        posts = Post.published.all()
        ser_data = PostSerializer(posts, many=True)
        # for i in posts:
        #     print(i.get_absolute_url)
        return Response(ser_data.data)
        # return render(request, "index.html", {"posts": posts})

class PostDetailView(APIView):
    def get(self, request, year, month, day, slug):
        post = get_list_or_404(Post,
                               status=Post.Status.PUBLISHED,
                               slug=slug,
                               publish__year=year,
                               publish__month=month,
                               publish__day=day)
        ser_data = PostSerializer(post, many=True)
        return Response(ser_data.data)
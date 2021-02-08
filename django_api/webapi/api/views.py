from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        post = get_object_or_404(self.get_queryset(), pk=post_id)
        return Response(self.get_serializer(post).data)

    def perform_update(self, serializer):
        post_id = self.kwargs['pk']
        author = self.get_queryset().get(pk=post_id).author
        if self.request.user != author:
            return Response(status.HTTP_403_FORBIDDEN)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        post = get_object_or_404(self.get_queryset(), pk=post_id)
        if self.request.user != post.author:
            return Response(status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = self.kwargs['post_id']
        post = Post.objects.get(pk=post)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post, author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(self.get_queryset(), pk=comment_id)
        return Response(self.get_serializer(comment).data)

    def perform_update(self, serializer):
        comment_id = self.kwargs['pk']
        author = self.get_queryset().get(pk=comment_id).author
        if self.request.user != author:
            return Response(status.HTTP_403_FORBIDDEN)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(self.get_queryset(), pk=comment_id)
        if self.request.user != comment.author:
            return Response(status.HTTP_403_FORBIDDEN)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)

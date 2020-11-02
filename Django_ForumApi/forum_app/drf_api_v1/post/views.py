# i18n
from django.utils.translation import ugettext as _
# exceptions
from django.core.exceptions import FieldError
# rest_framework view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
# permission
from rest_framework.permissions import IsAuthenticated
from ..member.permissions import IsOwner, IsAdminOrOwner
# pagination
from rest_framework.pagination import CursorPagination
# tools
from ..tools import get_user_or_404
# Model & Serializer
from django.contrib.auth import get_user_model
from forum_app.models import Post, Member
from .serializer import PostSerializer, ReadPostSerializer

User = get_user_model()

class CreateOrListPost(APIView):
    DEFAULT_PAGE_SIZE = 20
    class CursorPaginator(CursorPagination):
        ordering = "-date_created"
        cursor_query_param = "c"

    def get(self, request, *args, **kwargs):
        self.serializer_class = ReadPostSerializer
        self.permission_classes = [ IsAuthenticated ]
        self.check_permissions(request)

        paginator = self.CursorPaginator()
        paginator.page_size = self.DEFAULT_PAGE_SIZE
        ordering = request.query_params.get("ordering", None)
        page_size = request.query_params.get("page_size", None)

        if ordering:
            paginator.ordering = ordering
        if page_size:
            try:
                paginator.page_size = int(page_size)
            except ValueError as err:
                return Response(
                    {"detail": _("You must provide number, not '{}'").format(page_size)},
                    status=HTTP_400_BAD_REQUEST
                )
        
        posts = Post.objects.all()

        try:
            posts_page = paginator.paginate_queryset(posts, request)
        except FieldError as err:
            return Response({"detail": str(err)}, status=HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(posts_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        self.serializer_class = PostSerializer
        self.permission_classes = [ IsAuthenticated ]
        self.check_permissions(request)

        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return Response({"detail": _("This user instance is not a member.")}, status=HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data["content"]
        new_post = Post.objects.create(content=content, writer=member)

        return Response(serializer.data, status=HTTP_201_CREATED)

class ReadUpdateDeletePost(APIView):
    def get(self, request, postid):
        self.permission_classes = [ IsAuthenticated ]
        self.check_permissions(request)
        self.serializer_class = ReadPostSerializer

        try:
            post = Post.objects.get(id=postid)
        except Post.DoesNotExist:
            return Response({"detail": _("The resource you're looking for does not exists.")}, status=HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(post)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, postid):
        self.permission_classes = [IsOwner]
        self.serializer_class = PostSerializer
        post = None

        try:
            post = Post.objects.get(id=postid)
            self.check_object_permissions(request, post.writer.user)

        except Post.DoesNotExist:
            return Response({"detail": _("This post does not exists.")}, status=HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        post.content = serializer.validated_data['content']
        post.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, postid):
        self.permission_classes = [IsAdminOrOwner]
        try:
            post = Post.objects.get(id=postid)
            self.check_object_permissions(request, post.writer.user)
        except Post.DoesNotExist:
            return Response({"detail": _("This post does not exists.")}, status=HTTP_404_NOT_FOUND)
        # perform deletion
        post.delete()
        return Response({"detail":"Post deleted."}, status=HTTP_204_NO_CONTENT)    
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import CursorPagination

from forum_app.models import Post, Member
from .serializer import PostSerializer


class CreatePost(APIView):
    DEFAULT_PAGE_SIZE = 2
    class CursorPaginator(CursorPagination):
        ordering = "-date_created"
        cursor_query_param = "c"

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        paginator = self.CursorPaginator()
        paginator.page_size = self.DEFAULT_PAGE_SIZE
        ordering = request.query_params.get("ordering", None)
        page_size = request.query_params.get("page_size", None)
        if ordering:
            paginator.ordering = ordering
        if page_size:
            try:
                paginator.page_size = int(page_size)
            except ValueError:
                paginator.page_size = self.DEFAULT_PAGE_SIZE

        posts = Post.objects.all()
        posts_page = paginator.paginate_queryset(posts, request)
        serializer = self.serializer_class(posts_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        
    def post(self, request):
        self.check_permissions(request)
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExists:
            return Response({"message": _("This user instance is not a member.")}, status=HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data["content"]
        new_post = Post.objects.create(content=content, writer=member)
        return Response(serializer.data, status=HTTP_200_OK)
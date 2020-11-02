# auth
from django.contrib.auth import get_user_model, login, logout
# i18n
from django.utils.translation import ugettext as _
# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
)
# tools
from ..tools import generate_username, get_user_or_404
# permission
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
# models and serializer
from forum_app.models import (
    Member,
    Post
)
from .serializer import (
    CreateMemberSerializer,
    ReadMemberSerializer,
    LoginSerializer,
)
# Get the JWT settings, add these lines after the import/from lines
from datetime import datetime
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class CreateMember(APIView):
    serializer_class = CreateMemberSerializer
    def post(self, request):
        def _create(validated_data):
            # do not directly modify validated_data (it's used by serializer internally)
            validated_data = validated_data.copy()
            user = validated_data.pop('user')
            first_name = user['first_name']
            last_name = user['last_name']
            email = user['email']
            password = validated_data.pop('password')
            confirm_password = validated_data.pop('confirm_password')
            #django user model
            username = generate_username(first_name, last_name)
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)
            # change to False if want to implement email confirmation
            user.is_active = True
            user.save()
            #member model that extends user
            instance = Member.objects.create(user=user, **validated_data)
            return instance

        serializer = self.serializer_class(
            data=request.data, 
            context={
                'request': request, 
            }
        )
        serializer.is_valid(raise_exception=True)
        _create(serializer.validated_data)
        return Response(serializer.data, status=HTTP_201_CREATED)

class ReadUpdateDeleteMember(APIView):
    """Use **get** to **Read**, **put** to **Update**, **delete** to **Delete**"""
    serializer_class = CreateMemberSerializer
    def get(self, request, *args, **kwargs):
        self.permission_classes = [ IsAuthenticated ]
        query_user = get_user_or_404(self.kwargs['username'])
        member = Member.objects.get(user=query_user)
        self.check_permissions(request)

        serializer = ReadMemberSerializer(member)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        def _update(validated_data):
            # do not directly modify validated_data (it's used by serializer internally)
            validated_data = validated_data.copy()
            user = validated_data.pop('user')
            first_name = user['first_name']
            last_name = user['last_name']
            email = user['email']
            password = validated_data.pop('password')
            confirm_password = validated_data.pop('confirm_password')
            #django user model
            user = User.objects.get(username = self.kwargs['username']);
            user.first_name=first_name
            user.last_name=last_name
            user.last_name=last_name
            user.email=email
            user.set_password(password)
            # change to False if want to implement email confirmation
            user.is_active = True
            user.save()
            #member model that extends user
            instance = Member.objects.filter(user=user).update(**validated_data)
            return instance

        self.permission_classes = [ IsOwner ]
        query_user = get_user_or_404(self.kwargs['username'])
        member = Member.objects.get(user=query_user)
        self.check_object_permissions(request, member.user)
        serializer = self.serializer_class(
            data=request.data, 
            context={
                'request': request, 
                'username': self.kwargs['username']
            }
        )
        serializer.is_valid(raise_exception=True)
        _update(serializer.validated_data)
        return Response(serializer.data, status=HTTP_201_CREATED)

class Login(APIView):
    """To login user must provide either email or username with password"""
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data.get("email", None)
        username = validated_data.get("username", None)
        password = validated_data.get("password")
        user = None
        member = None
        try:
            if email:
                user = User.objects.get(email=email)
            if (not user) and username:
                user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"detail": _("Login failed. Check your login credentials.")}, status=HTTP_400_BAD_REQUEST)
            member = Member.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"detail": _("Login failed. Check your login credentials.")}, status=HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            return Response({"detail": _("This user does not have member credentials.")}, status=HTTP_400_BAD_REQUEST)
        
        # user credentials valid perform authenticate
        # generate jwt token
        token = jwt_encode_handler(jwt_payload_handler(user))
        login(request, user)

        roles = {
            "regular":[
                {"post":{
                    "actions":[
                        "Create:Self", 
                        "Read:All", 
                        "Update:Self", 
                        "Delete:Self"
                    ],
                    }
                }
            ],
            "admin":[
                {"post":{
                    "actions":[
                        "Create:Self", 
                        "Read:All", 
                        "Update:Self", 
                        "Delete:All"
                    ],
                    }
                }
            ],
        }
        
        response_data = {
            "username":user.username,
            "full_name":f"{user.first_name} {user.last_name}",
            "birth_date": member.birth_date,
            "birth_place": member.birth_place,
            "gender": member.gender,
            "type": member.types,
            "token": token,
            "roles": roles[member.types],
        }
        response = Response(response_data, status=HTTP_200_OK)

        if api_settings.JWT_AUTH_COOKIE:
            expiration = (
                datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
            )
            response.set_cookie(
                api_settings.JWT_AUTH_COOKIE,
                token,
                expires=expiration,
                httponly=True
            )
        return response

class Logout(APIView):
    def get(self, request):
        """Logout the current session."""
        
        logout(request)

        response = Response({'detail': 'logout successful.'})
        if api_settings.JWT_AUTH_COOKIE:
            response.delete_cookie(api_settings.JWT_AUTH_COOKIE)
        return response